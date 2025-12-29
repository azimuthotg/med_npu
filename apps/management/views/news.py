"""
News management views
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from apps.management.mixins import NewsPermissionMixin
from apps.news.models import News, Category


class NewsListView(NewsPermissionMixin, ListView):
    """รายการข่าวทั้งหมด พร้อม search และ filter"""
    model = News
    template_name = 'management/news/list.html'
    context_object_name = 'news_list'
    paginate_by = 20
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )

        # Filter by category
        category_id = self.request.GET.get('category', '').strip()
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status == 'published':
            queryset = queryset.filter(is_published=True)
        elif status == 'draft':
            queryset = queryset.filter(is_published=False)

        # Filter by featured
        featured = self.request.GET.get('featured', '').strip()
        if featured == '1':
            queryset = queryset.filter(is_featured=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_featured'] = self.request.GET.get('featured', '')

        # Statistics
        context['total_news'] = News.objects.count()
        context['published_news'] = News.objects.filter(is_published=True).count()
        context['draft_news'] = News.objects.filter(is_published=False).count()

        return context


class NewsCreateView(NewsPermissionMixin, CreateView):
    """สร้างข่าวใหม่"""
    model = News
    template_name = 'management/news/form.html'
    fields = [
        'title', 'category', 'gallery', 'excerpt', 'content',
        'featured_image', 'is_published', 'is_featured',
        'published_at', 'meta_description'
    ]
    success_url = reverse_lazy('management:news_list')

    def form_valid(self, form):
        messages.success(self.request, f'สร้างข่าว "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'สร้างข่าวใหม่'
        context['submit_text'] = 'บันทึกข่าว'
        return context


class NewsUpdateView(NewsPermissionMixin, UpdateView):
    """แก้ไขข่าว"""
    model = News
    template_name = 'management/news/form.html'
    fields = [
        'title', 'category', 'gallery', 'excerpt', 'content',
        'featured_image', 'is_published', 'is_featured',
        'published_at', 'meta_description'
    ]
    success_url = reverse_lazy('management:news_list')

    def form_valid(self, form):
        messages.success(self.request, f'แก้ไขข่าว "{form.instance.title}" สำเร็จ')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'แก้ไขข่าว: {self.object.title}'
        context['submit_text'] = 'บันทึกการแก้ไข'
        return context


class NewsDeleteView(NewsPermissionMixin, DeleteView):
    """ลบข่าว"""
    model = News
    template_name = 'management/news/delete.html'
    success_url = reverse_lazy('management:news_list')

    def delete(self, request, *args, **kwargs):
        news_title = self.get_object().title
        messages.success(request, f'ลบข่าว "{news_title}" สำเร็จ')
        return super().delete(request, *args, **kwargs)
