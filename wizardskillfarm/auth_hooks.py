"""Hook into Alliance Auth"""

# Django
# from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

# AA Wizard Skill Farm
# AA Wizard Skill farm
from wizardskillfarm import urls


class WizardSkillFarmMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            ("Skill Farm"),
            "fas fa-cube fa-fw",
            "wizard-skillfarm:index",
            navactive=["wizardskillfarm:"],
        )

    def render(self, request):
        """Render the menu item"""

        if request.user.has_perm("wizardskillfarm.basic_access"):
            return MenuItemHook.render(self, request)

        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register the menu item"""

    return WizardSkillFarmMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register app urls"""

    return UrlHook(urls, "wizard-skillfarm", r"^wizard-skillfarm/")
