from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views import generic
from textform.models import Message
from comments.models import Comment
from .models import Blog
from .forms import BlogForm


class BlogView(generic.ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'latest_message_list'

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.blog = get_object_or_404(Blog.objects.all(), pk=pk)

        self.form = BlogForm(request.GET)
        self.form.is_valid()

        self.search_field = self.form.cleaned_data.get('search')
        self.sort_field = self.form.cleaned_data.get('sort')

        return super(BlogView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def get_queryset(self):
        messages = super(BlogView, self).get_queryset()
        if self.request.user.is_authenticated():
            messages = Message.objects.filter(Q(published=True) | Q(author=self.request.user)) \
                .order_by('-pub_date').order_by('published')
        else:
            messages = Message.objects.filter(Q(published=True)).order_by('-pub_date')

        if self.search_field:
            messages = messages.filter(Q(title__icontains=self.search_field) | Q(text__icontains=self.search_field))
        if self.sort_field:
            messages = messages.order_by(self.sort_field)
        return messages.filter(Q(blog=self.blog))

    def latest_comments(self):
        print self.blog.message_set
        return Comment.objects.filter(Q(message__in=self.blog.message_set.all())).order_by('-pub_date')[:7]
        #.filter(Q(message__in=self.blog.message_set))