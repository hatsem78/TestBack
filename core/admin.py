from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib import admin
from django.contrib.auth.models import Permission

from api.report_powerbi.library.import_report import Imports
from api.report_powerbi.library.work_spase import WorkSpace
from core import models
from passlib.hash import pbkdf2_sha256 as sha256

from core.models import (
    PartOfDay,
    Chanel,
    Advertise,
    StatisticsTva,
    ClientBench,
    Source,
    TvaModule,
    UserProfile,
    UserPowerBi,
    Campaign,
    TypeOfAd,
    Simulator,
    ImportFile,
    ConfigruationAdvertiser,
    PowerbiWorkSpace,
    MenuPowerBi,
    SystemConfig,
    Media,
    FeatureType,

    Feature, Betas, Alphas, Sales, ValuesForcasted, AdsTocks, SimulatorCalculator, Constants, MixSalesEvolution,
    CostPerUnitSoldRoas, Seasonality, Competition, Precition, ConversionType, MtaResult, Invesment,
    PathAnalisisTouchpoint, PathAnalisisChannels, PathsMetrics, CoalitionsMetrics, Irma, DataStudioWorkSpace,
    DataStudoMenu, UserDataStudio, AdvertirserInsights, UploadFilesModule)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    filter_horizontal = ("module",)


class UserPowerBiInline(admin.StackedInline):
    model = UserPowerBi
    filter_horizontal = ("powerbi_work_space", )


class UserDataStudioInline(admin.StackedInline):
    model = UserDataStudio
    filter_horizontal = ("data_studio_work_space", )

class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "name"]
    fieldsets = (
        #(None, {"fields": ("email", "password", "groups")}),
        #(None, {"fields": ("email", "password", "groups")}),
        (_("Personal info"), {"fields": (
            "email", "password", "name", "last_name", "country", "department")
        }),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", 'is_havas')}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
        (_("Personal info"), {"fields": (
           "name", "last_name", "country", "department")
        }),
    )
    inlines = [UserProfileInline, UserPowerBiInline, UserDataStudioInline]


class StatisticsTvaAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "advertiser",
        "date_time",
        "part_day",
        "name_creative",
        "source",
        "client_bench",
        "campaign",
        "channel",
        "length",
        "impressions",
        "lift_percentage",
        "lift_abs",
        "show",
        "reaction_rate",
        "response",
        "session",
        "creative",
        "type_of_ad",
        "break_position",
        "get_log"
    )
    list_display = (
        "id",
        "advertiser",
        "date_time",
        "part_day",
        "name_creative",
        "source",
        "client_bench",
        "campaign",
        "channel",
        "length",
        "impressions",
        "lift_percentage",
        "lift_abs",
        "show",
        "reaction_rate",
        "response",
        "session",
        "creative",
        "type_of_ad",
        "break_position",
        "get_log"
    )


class CampaignAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "advertiser", "campaign_name")
    search_fields = ("id", "name", "campaign_name")
    model = Campaign
    filter_horizontal = ("module",)
    #filter_horizontal = ("module",)


class AdvertiserAdmin(admin.ModelAdmin):
    model = Advertiser
    list_display = ('id', "countries", "name")
    search_fields = ("countries", "name")
    list_filter = ("name",)
    ordering = ("-name",)
    filter_horizontal = ("user",)


class SimulatorAdmin(admin.ModelAdmin):
    model = Simulator
    list_display = ("id", "advertiser", "scenario_name", "scenario_info")
    search_fields = ("id", "advertiser", "scenario_name", "scenario_info")
    list_filter = ("scenario_name",)
    ordering = ("-scenario_name",)


class TvaModuleAdmin(admin.ModelAdmin):
    model = TvaModule
    list_display = ("id", "name", "menu")
    search_fields = ("id", "name", "menu")
    list_filter = ("name",'menu')
    filter_horizontal = ("country",)
    ordering = ("-menu",)


class TypeOfAdAdmin(admin.ModelAdmin):
    model = TypeOfAd
    list_display = ("id", "name", "advertiser")
    search_fields = ("id", "name", "advertiser")
    list_filter = ("name",'advertiser')
    ordering = ("-advertiser",)


class PartOfDayAdAdmin(admin.ModelAdmin):
    model = PartOfDay
    list_display = ("id", "name", "name_description")
    search_fields = ("id", "name", "name_description")
    list_filter = ("name",'name_description')
    ordering = ("-name",)


class ChanelDayAdAdmin(admin.ModelAdmin):
    model = Chanel
    list_display = ("id", "name", "advertiser_id")
    search_fields = ("id", "name", "advertiser_id")
    list_filter = ("name",'advertiser_id')
    ordering = ("-advertiser_id",)


class ImportFileAdmin(admin.ModelAdmin):
    model = ImportFile
    
    list_display = ("id", "advertiser", "date_time", "name_file", "campaign_name", "source", "module", "start_time", "end_time", "log_info")
    search_fields = ("id", "advertiser", "date_time", "name_file", "campaign_name", "source", "module", "start_time", "end_time", "log_info")
    list_filter = ("advertiser", "module", "campaign_name", "log_info")
    ordering = ("-advertiser",  "module", "campaign_name", "log_info")


class ConfigruationAdvertiserAdmin(admin.ModelAdmin):
    model = ConfigruationAdvertiser
    
    list_display = ("id", "enabled", "advertiser", "date_time", "date_time_update", "name_configuration", "configuration")
    search_fields = ("id","enabled", "advertiser", "date_time", "date_time_update", "name_configuration", "configuration")
    list_filter = ("advertiser","enabled", "name_configuration", "configuration", )
    ordering = ("-name_configuration", "enabled", "advertiser", "configuration", )


class PowerbiWorkSpaceAdmin(admin.ModelAdmin, WorkSpace):
    model = PowerbiWorkSpace
    list_display = ("id", "work_space", "name_work_space", "id_work_space_pwbi")
    list_filter = ("work_space", "name_work_space", "id_work_space_pwbi")
    search_fields = ("id", "work_space", "name_work_space", "id_work_space_pwbi")
    #readonly_fields = ("id_work_space_pwbi", )
    ordering = ("-work_space", "-id_work_space_pwbi",)

    def save_model(self, request, obj, form, change):
        if change:
            self.patch_work_space(id=obj.id_work_space_pwbi, name=obj.work_space)
        obj.save()

    def delete_model(self, request, obj):
        obj.delete()
        msg = self.delete_work_space(id=obj.id_work_space_pwbi)


class MenuPowerBiAdmin(admin.ModelAdmin, Imports):
    model = MenuPowerBi
    list_display = ("id", "enabled", "page", 'order_menu', "advertiser", "work_spaces", "id_report", "name", "menu", "description" )
    list_filter = ("advertiser", "work_spaces", "id_report", "name", "menu", "description")
    search_fields = ("id", "advertiser", "work_spaces", "id_report", "name", "menu", "description")
    # readonly_fields = ("id_report", "file_report")
    readonly_fields = ("id_dataset", "id_report")
    ordering = ("advertiser", "work_spaces", "name", 'order_menu' )

    def save_model(self, request, obj, form, change):
        if obj.file_report != '':
            result = self.upload_file(
                filename= obj.file_report,
                dataset_displayname=obj.name.strip().replace('%20', '_'),
                group_id=obj.work_spaces.id_work_space_pwbi,
                id_report=obj.id_report,
                id_dataset=obj.id_dataset
            )
            obj.id_report = result['id_report']
            obj.id_dataset = result['id_dataset']

        obj.save()

    def delete_model(self, request, obj):

        if obj.id_report != '' or obj.id_report is None:
            self.delete_report(obj.work_spaces.id_work_space_pwbi, obj.id_report)

        if obj.id_dataset != '' or obj.id_dataset is None:
            self.delete_dataset(obj.work_spaces.id_work_space_pwbi, obj.id_dataset)

        obj.delete()

class SystemConfigAdmin(admin.ModelAdmin):
    model = SystemConfig
    list_display = ("id", "type_config", "name_configuration", "date_time", "date_time_update", "configuration")

    def configurations(self, obj):
        return sha256.decode(obj.configuration)

    list_filter = ( "type_config",  "name_configuration", "date_time", "date_time_update", "configuration")
    
    search_fields = ("id", "type_config", "name_configuration", "date_time", "date_time_update", "configuration")

    ordering = ("-name_configuration",)


class MediaAdmin(admin.ModelAdmin):
    model = Media
    list_display = ("id", "advertiser", "name", "description")

    list_filter = ("advertiser", "name", "description")

    search_fields = ("id", "advertiser", "name", "description")

    ordering = ("-advertiser", )


class FeatureTypeAdmin(admin.ModelAdmin):
    model = FeatureType
    list_display = ("id", "advertiser", "name", "description")

    list_filter = ("advertiser", "name", "description")

    search_fields = ("id", "advertiser", "name", "description")

    ordering = ("-advertiser", )


class FeatureAdmin(admin.ModelAdmin):
    model = Feature
    list_display = ("id", "advertiser", "feature_type", "name", "description", "get_log")

    list_filter = ("advertiser", "feature_type", "name", "description")

    search_fields = ("id", "advertiser", "feature_type", "name", "description", "get_log")

    ordering = ("-advertiser", "feature_type", "name")


class BetasAdmin(admin.ModelAdmin):
    model = Betas
    list_display = ("id", "advertiser", "campaign", "feature", "beta", "pvalue", "get_log")

    list_filter = ("advertiser", "campaign", "feature", "beta")

    search_fields = ("id", "advertiser", "campaign", "feature",  "pvalue")

    ordering = ("-advertiser", "campaign", "feature", )


class AlphasAdmin(admin.ModelAdmin):
    model = Alphas
    list_display = ("id", "advertiser", "campaign", "media", "alpha", "get_log")

    list_filter = ("advertiser", "campaign", "media", "alpha")

    search_fields = ("id", "advertiser", "campaign", "media", "alpha")

    ordering = ("-advertiser", "media", "campaign", )


class SalesAdmin(admin.ModelAdmin):
    model = Sales
    list_display = ("id", "advertiser", "campaign", "date", "sale", "get_log")

    list_filter = ("advertiser", "campaign", "date")

    search_fields = ("id", "advertiser", "campaign", "date", "sale", "get_log")

    ordering = ("-advertiser", "campaign", "date", )


class ValuesForcastedAdmin(admin.ModelAdmin):
    model = ValuesForcasted
    list_display = ("id", "advertiser", "campaign", "feature", "feature_type", "date", "week_month", "inv_original", "value",
                    "sale_forecasted", "get_log")

    list_filter = ("advertiser", "campaign", "feature", "feature_type", "date", "week_month")

    search_fields = ("id", "advertiser", "campaign", "feature", "feature_type", "date", "week_month", "inv_original", "value",
                     "sale_forecasted", "get_log")

    ordering = ("-advertiser", "campaign", "feature", "feature_type", "date")


class AdsTocksAdmin(admin.ModelAdmin):
    model = AdsTocks
    list_display = ("id", "advertiser", "media", "dragged_adstocks", "original_adstocks", "original_investment",
                    "calculated_adstocks", "get_log"
                    )

    list_filter = ("advertiser", "media", )

    search_fields = ("id", "advertiser", "media", "dragged_adstocks", "original_adstocks", "original_investment",
                     "calculated_adstocks", "get_log"
                     )

    ordering = ("-advertiser", "media", )


class SimulatorCalculatorAdmin(admin.ModelAdmin):
    model = SimulatorCalculator
    list_display = ("id", "advertiser", "item", "edit", "hitorical", "beta", "forcasted", "forcasted_sales_feature",
                    "get_log"
                    )

    list_filter = ("advertiser", "item", "edit", "hitorical", "beta", "forcasted", "forcasted_sales_feature")

    search_fields = ("id", "advertiser", "item", "edit", "hitorical", "beta", "forcasted", "forcasted_sales_feature",
                     "get_log"
                    )

    ordering = ("-advertiser", "item", "edit", )


class ConstantsAdmin(admin.ModelAdmin):
    model = Constants
    list_display = ("id", "advertiser", "constant", "get_log")

    list_filter = ("advertiser", "constant")

    search_fields = ("id", "advertiser", "get_log")

    ordering = ("-advertiser", "constant", )


class MixSalesEvolutionAdmin(admin.ModelAdmin):
    model = MixSalesEvolution
    list_display = ("id", "advertiser", "media", "date", "value", "get_log")

    list_filter = ("advertiser", "media")

    search_fields = ("id", "media", "date", "value", "get_log")

    ordering = ("-advertiser", "media", "date", )


class CostPerUnitSoldRoasAdmin(admin.ModelAdmin):
    model = CostPerUnitSoldRoas
    list_display = ("id", "advertiser", "media", "date", "cost_per_unit_sold", "roas", "get_log")

    list_filter = ("advertiser", "media", "date", "cost_per_unit_sold", "roas")

    search_fields = ("id", "media", "date", "cost_per_unit_sold", "roas", "get_log")

    ordering = ("-advertiser", "media", "date", )


class SeasonalityAdmin(admin.ModelAdmin):
    model = Seasonality
    list_display = ("id", "advertiser", "date", "baseline_value", "seasonality_value", "get_log")

    list_filter = ("advertiser", "date")

    search_fields = ("id", "date", "baseline_value", "seasonality_value", "get_log")

    ordering = ("-advertiser", "date", )


class CompetitionAdmin(admin.ModelAdmin):
    model = Competition
    list_display = ("id", "advertiser", "feature", "date", "value")

    list_filter = ("advertiser", "feature")

    search_fields = ("advertiser", "feature", "date", "value")

    ordering = ("-advertiser", "feature", "date", )


class PrecitionAdmin(admin.ModelAdmin):
    model = Competition
    list_display = ("id", "advertiser", "date", "reale_sales", "forcasted_sales", "get_log")

    list_filter = ("advertiser", "date")

    search_fields = ("id", "advertiser", "date", "forcasted_sales", "get_log")

    ordering = ("-advertiser",  "date", )


class ConversionTypeAdmin(admin.ModelAdmin):
    model = ConversionType
    list_display = ("id", "advertiser", "campaign", "conversion_type", "description")

    list_filter = ("advertiser",  "campaign", "conversion_type", "description")

    search_fields = ("id", "advertiser", "campaign",  "conversion_type")

    ordering = ("-advertiser",  "campaign", "conversion_type",)


class MtaResultAdmin(admin.ModelAdmin):
    model = MtaResult
    list_display = (
        "id", "advertiser", "campaign", "date", "conversion_type", "channel", "revenue_shapley",
        "atributed_conversion_shapley", "atributed_conversiones_lineal", "revenue_linear",
        "revenue_first_click", "revenue_last_click", "stimuli_quantity_paths", "paths_quantity",
        "assistances_role", "conversion_role", "acquisition_role", "shapley", "this_type_conversions",
        "convertion_paths_with_this_channel",  "daily_impulses", "get_log"
    )

    list_filter = (
        "advertiser", "campaign", "date", "conversion_type", "channel"
    )

    search_fields = (
        "id", "advertiser", "campaign", "date", "conversion_type", "channel", "revenue_shapley",
         "atributed_conversion_shapley", "atributed_conversiones_lineal", "revenue_linear",
         "revenue_first_click", "revenue_last_click", "stimuli_quantity_paths", "paths_quantity",
         "assistances_role", "conversion_role", "acquisition_role", "shapley", "this_type_conversions",
         "convertion_paths_with_this_channel", "daily_impulses", "get_log"
     )

    ordering = ("-advertiser", "campaign", "conversion_type", "channel")


class InvesmentAdmin(admin.ModelAdmin):
    model = Invesment
    list_display = (
        "id", "date", "advertiser", "campaign", "channel", "invesment"
    )

    list_filter = (
        "date", "advertiser", "campaign", "channel", "invesment"
    )

    search_fields = (
        "id", "date", "advertiser", "campaign", "channel", "invesment"
    )

    ordering = ("-advertiser", "date", "campaign", )


class PathsMetricsAdmin(admin.ModelAdmin):
    model = Invesment
    list_display = (
        "id", "date", "advertiser", "campaign", "total_paths"
    )

    list_filter = (
       "date", "advertiser", "campaign", "total_paths"
    )

    search_fields = (
        "id", "date", "advertiser", "campaign", "total_paths"
    )

    ordering = ("-advertiser", "date", "campaign", )


class PathAnalisisTouchpointAdmin(admin.ModelAdmin):
    model = PathAnalisisTouchpoint
    list_display = (
        "id", "date", "advertiser", "campaign", "conversion_type", "touchpoints_quantity", 'paths_count'
    )

    list_filter = (
        "date", "advertiser", "campaign", "conversion_type"
    )

    search_fields = (
        "id", "date",  "advertiser", "campaign", "conversion_type", "touchpoints_quantity", 'paths_count'
    )

    ordering = ("-advertiser", "date", "campaign", )


class PathAnalisisChannelsAdmin(admin.ModelAdmin):
    model = PathAnalisisTouchpoint
    list_display = (
        "id", "date", "advertiser", "campaign", "conversion_type", "channels_quantity", 'paths_count'
    )

    list_filter = (
       "date", "advertiser", "campaign", "conversion_type"
    )

    search_fields = (
        "id", "date",  "advertiser", "campaign", "conversion_type", "channels_quantity", 'paths_count'
    )

    ordering = ("-advertiser", "date", "campaign", )


class CoalitionsMetricsAdmin(admin.ModelAdmin):
    model = PathAnalisisTouchpoint
    list_display = (
        "id", "date", "advertiser", "campaign", "channel", "coalitions", 'len_coalitions',
        "total_paths", "conversion_paths", "conversion_rate", "channel_attribution"
    )

    list_filter = (
        "date", "advertiser", "campaign", "channel", "coalitions"
    )

    search_fields = (
        "id", "date",  "advertiser", "campaign", "channel", "coalitions", 'len_coalitions',
        "total_paths", "conversion_paths", "conversion_rate", "channel_attribution"
    )

    ordering = ("-advertiser", "date", "channel", )


class IrmaAdmin(admin.ModelAdmin):
    model = PathAnalisisTouchpoint
    list_display = (
        "id", "date", "advertiser", "campaign", "len_coalitions", "coalitions", 'conversion_volume', 'conversion_percentage',
        "possible_truncation", "zero_percentage", "ten_twenty_percentage", "twenty_thirty_percentage",
        "thirty_fourty_percentage", "fourty_fifty_percentage", "fifty_sixty_percentage", "sixty_seventy_percentage",
        "seventy_eighty_percentage", "eighty_ninety_percentage", "ninety_onehundred_percentage", "one_hundred_percentage",
        "total",
    )

    list_filter = (
        "date", "advertiser", "campaign", "len_coalitions", "coalitions"
    )

    search_fields = (
        "id", "date",  "advertiser", "campaign", "len_coalitions", "coalitions", 'conversion_volume', 'conversion_percentage',
        "possible_truncation", "zero_percentage", "ten_twenty_percentage", "twenty_thirty_percentage",
        "thirty_fourty_percentage", "fourty_fifty_percentage", "fifty_sixty_percentage", "sixty_seventy_percentage",
        "seventy_eighty_percentage", "eighty_ninety_percentage", "ninety_onehundred_percentage", "one_hundred_percentage",
        "total",
    )

    ordering = ("-advertiser", "date", "campaign", )


class DataStudioWorkSpaceAdmin(admin.ModelAdmin, WorkSpace):
    model = PowerbiWorkSpace
    list_display = ("id", "work_space", "name_work_space", "id_work_space_ds")
    list_filter = ("work_space", "name_work_space", "id_work_space_ds")
    search_fields = ("id", "work_space", "name_work_space", "id_work_space_ds")

    ordering = ("-work_space", "-id_work_space_ds",)

    def save_model(self, request, obj, form, change):
        obj.save()


class DataStudoMenuAdmin(admin.ModelAdmin, Imports):

    model = MenuPowerBi
    list_display = ("id", "enabled", 'order_menu', "advertiser", "work_spaces", "id_report", "name", "menu", 'url_report', "description")
    list_filter = ("advertiser", "work_spaces", "id_report", "name", "menu", "description")
    search_fields = ("id", "advertiser", "work_spaces", "id_report", "name", "menu", "description")
    # readonly_fields = ("id_report", "file_report")

    ordering = ("-advertiser", "-work_spaces", "-id_report", 'order_menu')


class AdvertirserInsightsAdmin(admin.ModelAdmin):

    model = AdvertirserInsights

    list_display = ("id", "enabled", "advertiser", "module", "menu", "sub_menu", "insights")
    list_filter = ("advertiser", "module", "menu", "sub_menu", "insights")
    search_fields = ("id", "advertiser", "module", "menu", "sub_menu", "insights")

    ordering = ("-advertiser", "-module", "menu")


class PermissionAdmin(admin.ModelAdmin):

    model = AdvertirserInsights

    list_display = ("id", "name", "content_type_id", "codename")
    list_filter = ("id", "name", "content_type_id", "codename")
    #search_fields = ("id", "advertiser", "module", "menu", "sub_menu", "insights")

    #ordering = ("-advertiser", "-module", "menu")


class UploadFilesModulesAdmin(admin.ModelAdmin):

    model = UploadFilesModule

    list_display = ("id", "file_name", "advertiser", "campaign", "module", "description", "url_file", "date_time", "status")
    ordering = ("-id", "-advertiser", "-module", "-campaign")


admin.site.register(models.User, UserAdmin)
admin.site.register(models.ConfigruationAdvertiser, ConfigruationAdvertiserAdmin)
admin.site.register(PartOfDay,PartOfDayAdAdmin)
admin.site.register(TypeOfAd, TypeOfAdAdmin)
admin.site.register(Chanel, ChanelDayAdAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
admin.site.register(Source)
admin.site.register(StatisticsTva, StatisticsTvaAdmin)
admin.site.register(ClientBench)
admin.site.register(TvaModule, TvaModuleAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Simulator, SimulatorAdmin)
admin.site.register(ImportFile, ImportFileAdmin)
admin.site.register(PowerbiWorkSpace, PowerbiWorkSpaceAdmin)
admin.site.register(MenuPowerBi, MenuPowerBiAdmin)
admin.site.register(SystemConfig, SystemConfigAdmin)


# Media Mix

admin.site.register(Media, MediaAdmin)
admin.site.register(FeatureType, FeatureTypeAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Betas, BetasAdmin)
admin.site.register(Alphas, AlphasAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(ValuesForcasted, ValuesForcastedAdmin)
admin.site.register(AdsTocks, AdsTocksAdmin)
admin.site.register(SimulatorCalculator, SimulatorCalculatorAdmin)
admin.site.register(Constants, ConstantsAdmin)
admin.site.register(MixSalesEvolution, MixSalesEvolutionAdmin)
admin.site.register(CostPerUnitSoldRoas, CostPerUnitSoldRoasAdmin)
admin.site.register(Seasonality, SeasonalityAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Precition, PrecitionAdmin)


# MTA
admin.site.register(ConversionType, ConversionTypeAdmin)
admin.site.register(MtaResult, MtaResultAdmin)
admin.site.register(Invesment, InvesmentAdmin)
admin.site.register(PathsMetrics, PathsMetricsAdmin)
admin.site.register(PathAnalisisTouchpoint, PathAnalisisTouchpointAdmin)
admin.site.register(PathAnalisisChannels, PathAnalisisChannelsAdmin)
admin.site.register(CoalitionsMetrics, CoalitionsMetricsAdmin)
admin.site.register(Irma, IrmaAdmin)


# Data Studio
admin.site.register(DataStudioWorkSpace, DataStudioWorkSpaceAdmin)
admin.site.register(DataStudoMenu, DataStudoMenuAdmin)


# Configuration modules


admin.site.register(Permission, PermissionAdmin)
admin.site.register(AdvertirserInsights, AdvertirserInsightsAdmin)


admin.site.register(UploadFilesModule, UploadFilesModulesAdmin)









