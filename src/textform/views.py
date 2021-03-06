from django.shortcuts import get_object_or_404, resolve_url
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
from django.db.models import Q
from django.views import generic
from .models import Message
from .forms import IndexForm, MessageForm
from comments.models import Comment
from django.db.models import Count
from urllib2 import HTTPError
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class IndexView(generic.ListView):
    template_name = 'textform/index.html'
    context_object_name = 'latest_message_list'
    fields = ('author', 'title', 'text', 'blog', 'tags')
    model = Message

    def dispatch(self, request, *args, **kwargs):

        self.form = IndexForm(request.GET)
        self.form.is_valid()

        self.search_field = self.form.cleaned_data.get('search')
        self.sort_field = self.form.cleaned_data.get('sort')

        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['latest_comments'] = Comment.objects.order_by('-pub_date')[:7]
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            messages = Message.objects.filter(Q(published=True) | Q(author=self.request.user)) \
                .order_by('-pub_date').order_by('published')
        else:
            messages = Message.objects.filter(Q(published=True)).order_by('-pub_date')

        if self.search_field:
            messages = messages.filter(Q(title__icontains=self.search_field) | Q(text__icontains=self.search_field))

        messages = messages.annotate(comments_count=Count('comment__id'))
        if self.sort_field:
            messages = messages.order_by(self.sort_field)
        return messages



class MessageView(generic.CreateView):
    template_name = 'textform/detail.html'
    model = Comment
    fields = ('text',)
    context_object_name = 'comment'

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.message = get_object_or_404(Message.objects.all(), pk=pk)
        return super(MessageView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.message = self.message
        form.instance.author = self.request.user
        return super(MessageView, self).form_valid(form)

    def get_success_url(self):
        return resolve_url("textform:detail", pk=self.message.id)

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['message'] = self.message
        return context

def upmessage(request):
    message_id = None
    if request.method == 'GET':
        message_id = request.GET['message_id']

    data = {"success": True, "likes": 0}
    if message_id:
        message = Message.objects.get(id=int(message_id))
        if message:
            message.like_count += 1
            message.save()
            data["likes"] = message.like_count
        else:
            data["success"] = False
    else:
        data["success"] = False
    return JsonResponse(data)


class NewMessageView(generic.CreateView):
    template_name = 'textform/printMessage.html'
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return resolve_url('textform:detail', self.object.pk)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewMessageView, self).form_valid(form)

    def get_initial(self):
        if self.request.method == 'GET':
            if not self.request.user.is_authenticated():
                raise HTTPError


class EditMessageView(generic.UpdateView):
    template_name = 'textform/editMessage.html'
    model = Message
    max_tag_number = 3
    fields = ('title', 'text', 'blog', 'tags')

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    def get_success_url(self):
        return resolve_url('textform:detail', self.object.pk)

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(EditMessageView, self).form_valid(form)

def deletemessage(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.published = False
    message.save()
    return HttpResponseRedirect(reverse('textform:index'))


