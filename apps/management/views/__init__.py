from .auth import ManagementLoginView, ManagementLogoutView
from .dashboard import DashboardView
from .news import NewsListView, NewsCreateView, NewsUpdateView, NewsDeleteView
from .categories import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from .gallery import (
    GalleryListView, GalleryCreateView, GalleryUpdateView, GalleryDeleteView,
    GalleryImageManageView, GalleryImageCreateView, GalleryImageUpdateView, GalleryImageDeleteView,
    GalleryBulkUploadView
)
from .executives import ExecutiveListView, ExecutiveCreateView, ExecutiveUpdateView, ExecutiveDeleteView
from .departments import DepartmentListView, DepartmentCreateView, DepartmentUpdateView, DepartmentDeleteView
from .programs import (
    ProgramListView, ProgramCreateView, ProgramUpdateView, ProgramDeleteView,
    AdmissionListView, AdmissionCreateView, AdmissionUpdateView, AdmissionDeleteView
)
from .banners import BannerListView, BannerCreateView, BannerUpdateView, BannerDeleteView
from .popups import PopupListView, PopupCreateView, PopupUpdateView, PopupDeleteView
from .settings import SiteSettingsView

__all__ = [
    'ManagementLoginView',
    'ManagementLogoutView',
    'DashboardView',
    'NewsListView',
    'NewsCreateView',
    'NewsUpdateView',
    'NewsDeleteView',
    'CategoryListView',
    'CategoryCreateView',
    'CategoryUpdateView',
    'CategoryDeleteView',
    'GalleryListView',
    'GalleryCreateView',
    'GalleryUpdateView',
    'GalleryDeleteView',
    'GalleryImageManageView',
    'GalleryImageCreateView',
    'GalleryImageUpdateView',
    'GalleryImageDeleteView',
    'GalleryBulkUploadView',
    'ExecutiveListView',
    'ExecutiveCreateView',
    'ExecutiveUpdateView',
    'ExecutiveDeleteView',
    'DepartmentListView',
    'DepartmentCreateView',
    'DepartmentUpdateView',
    'DepartmentDeleteView',
    'ProgramListView',
    'ProgramCreateView',
    'ProgramUpdateView',
    'ProgramDeleteView',
    'AdmissionListView',
    'AdmissionCreateView',
    'AdmissionUpdateView',
    'AdmissionDeleteView',
    'BannerListView',
    'BannerCreateView',
    'BannerUpdateView',
    'BannerDeleteView',
    'PopupListView',
    'PopupCreateView',
    'PopupUpdateView',
    'PopupDeleteView',
    'SiteSettingsView',
]
