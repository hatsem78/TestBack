#! -.- coding: utf-8 -.-

import datetime
from pprint import pprint

from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from api.report_powerbi.library.work_spase import WorkSpace
from app import settings
from core.utils.crypt import Crypt


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        if self.is_havas:
            user.set_unusable_password()
        else:
            user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Countries(models.Model):

    class Meta:
        verbose_name_plural = "Countries"

    DEFAULT_PK = 11

    id = models.AutoField(primary_key=True, help_text="Unique id")
    iso_code  = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):

    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    country =  models.ForeignKey('Countries', related_name='User_Countries', on_delete=models.CASCADE,
                                   null=True, default=Countries.DEFAULT_PK)
    department = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_havas = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_advertiser(self):
        advertiser = Advertiser.objects.filter(user__id=self.id)
        data = []
        for element in advertiser:
            data.append({
                'id': element.id,
                'name': element.name
            })

        return data

    def get_module(self):
        modules = TvaModule.objects.filter(country__iso_code=self.country.iso_code)
        data = []
        for module in modules:
            data.append({
                'id': module.id,
                'name': module.name,
                'menu': module.menu
            })

        return data

    def save(self, *args, **kwargs):
        if self.is_havas:
            self.password = make_password(None)
        super().save(*args, **kwargs)


class PartOfDay(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact Precition"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50, blank=True)
    name_description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Advertiser(models.Model):

    class Meta:
        verbose_name_plural = "System Advertiser"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    countries = models.ForeignKey('Countries', related_name='Advertiser_Countries', on_delete=models.CASCADE,
                                null=True, default=Countries.DEFAULT_PK)
    name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #self.category = self.hero.category
        super().save(*args, **kwargs)


class Chanel(models.Model):

    class Meta:
        verbose_name_plural = "System Chanel"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50)
    advertiser = models.ForeignKey('Advertiser', related_name='Chanel_Advertiser', on_delete=models.CASCADE,
                                      null=True)

    def __str__(self):
        return self.name


class Source(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact Source"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class ClientBench(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact ClientBench"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    brand = models.CharField(max_length=100, blank=True)
    competitor = models.CharField(max_length=30, blank=True)
    advertiser = models.ForeignKey('Advertiser', related_name='ClientBench_Advertiser', on_delete=models.CASCADE,
                                      null=True)

    @property
    def get_name(self):
        return '%s %s' % (self.brand, self.competitor)

    def __str__(self):
        return '%s %s' % (self.brand, self.competitor)


class TypeOfAd(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact TypeOfAd"

    """Type Of Ad"""
    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50, blank=True)
    advertiser = models.ForeignKey('Advertiser', related_name='TypeOfAd_Advertiser', on_delete=models.CASCADE,
                                   null=True, blank=True)

    def __str__(self):
        return self.name


class StatisticsTva(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact StatisticsTva"

    """Table Statistics the tva """
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser',  on_delete=models.CASCADE,
                                   null=True)
    date_time = models.DateTimeField(blank=True, editable=True)
    part_day = models.ForeignKey('PartOfDay', related_name='statistics_partofday', on_delete=models.CASCADE, null=True)
    name_creative = models.CharField(max_length=200, blank=True, null=True, db_index=True, help_text="Name Creative", )
    source = models.ForeignKey('Source', related_name='statistics_program', on_delete=models.CASCADE, null=True)
    client_bench = models.OneToOneField(ClientBench, on_delete=models.SET_NULL, related_name='statistics_clientbench',
                                        null=True, blank=True)
    campaign = models.ForeignKey('Campaign', related_name='StatisticsTva_Campaign', on_delete=models.CASCADE, null=True)
    channel = models.ForeignKey('Chanel', related_name='statistics_chanel', on_delete=models.CASCADE, null=True)
    length = models.CharField(max_length=100, null=True, default='0.00', db_index=True, help_text="Length") 
    impressions = models.FloatField(default=0, blank=True, help_text="Impressions")
    lift_percentage = models.FloatField(default=0, blank=True, help_text="Lift Percentage")
    lift_abs = models.IntegerField(default=0, help_text="Lift Abs")
    show = models.CharField(max_length=200, null=False, db_index=True, help_text="Show")
    reaction_rate = models.FloatField(default=0, blank=True, help_text="Reaction Rate")
    response = models.FloatField(default=0, blank=True, help_text="Response")
    session = models.IntegerField(default=0, blank=True, help_text="session")
    creative = models.CharField(max_length=100, null=True, default='Unknow', db_index=True, help_text="Creative ")
    type_of_ad = models.ForeignKey('TypeOfAd', related_name='statistics_type_of_ad', on_delete=models.CASCADE, null=True)
    show_type = models.CharField(max_length=100, null=True, default='', db_index=True, help_text="Show Type")
    break_position  = models.CharField(max_length=100, null=True, default='unknown', db_index=True, help_text="Break Pposition")
    log = models.ForeignKey('ImportFile', related_name='StatisticsTva_ImportFile', on_delete=models.CASCADE, null=True)

    def get_date_time(self):
        date_time = datetime.datetime.strptime(str(self.date_time).replace('/', '-')[:19], '%Y-%m-%d %H:%M:%S')
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def get_advertiser_name(self):
        return self.advertiser.name

    @property
    def get_channel_name(self):
        return self.advertiser.name

    @property
    def get_client_bench(self):
        return self.client_bench.get_name

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class TvaModule(models.Model):

    class Meta:
        verbose_name_plural = "System Module"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50, blank=True)
    menu = models.CharField(max_length=50, blank=True)
    country = models.ManyToManyField(Countries, related_name='system_module_countries', blank=True)

    def __str__(self):
        return self.name


class PowerbiWorkSpace(models.Model, WorkSpace):

    class Meta:
        verbose_name_plural = "PowerBi WorkSpace"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    work_space = models.CharField(max_length=50, blank=True)
    name_work_space = models.CharField(max_length=50, blank=True)
    id_work_space_pwbi = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name_work_space

    def save(self, *args, **kwargs):

        if not self.id:
            self.id_work_space_pwbi = self.create_work_space(self.work_space)

        super().save(*args, **kwargs)

        
class MenuPowerBi(models.Model):
    class Meta:
        verbose_name_plural = "PowerBi Menu"

    enabled = models.BooleanField(default=False)
    page = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='MenuPowerBis_PowerbiWorkSpace', on_delete=models.CASCADE,
                                   null=True)
    work_spaces = models.ForeignKey('PowerbiWorkSpace', related_name='MenuPowerBis_Advertiser', on_delete=models.CASCADE,
                                   null=True)
    id_report = models.CharField(max_length=50, blank=True, default='')
    id_dataset  = models.CharField(max_length=50, blank=True, default='')
    name = models.CharField(max_length=50, blank=True)
    menu = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    file_report = models.FileField(default="", blank=True)
    order_menu = models.IntegerField(default=0, help_text="Order Menu")

    def __str__(self):
        return self.name

    def get_work_spaces(self):
        return self.work_spaces.work_space

    def save(self, *args, **kwargs):
        self.file_report = ''
        super().save(*args, **kwargs)


class UserPowerBi(models.Model):

    class Meta:
        verbose_name_plural = "PowerBi User"

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    powerbi_work_space = models.ManyToManyField(PowerbiWorkSpace, related_name='UserPowerBi_PowerbiWorkSpace', blank=True)
    
    def get_list_work_space_id(self, obj=None):
        list_work_space = self.powerbi_work_space.values_list('id')
        return list_work_space


class Campaign(models.Model):

    class Meta:
        verbose_name_plural = "Tv-Impact Campaign"

    """Type user Campaign"""
    id = models.AutoField(primary_key=True, help_text="Unique id")
    name = models.CharField(max_length=50, blank=True)
    advertiser = models.ForeignKey('Advertiser', related_name='Campaign_Advertiser', on_delete=models.CASCADE,
                                      null=True)
    module = models.ManyToManyField(TvaModule, related_name='Campaign_Advertiser_module', blank=True)
    campaign_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

    
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.ManyToManyField(TvaModule, related_name='UserProfile_module', blank=True)
    
    def get_modules(self, obj=None):
        return ", ".join(modules.menu.lower() for modules in self.module.all())


class Simulator(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Simulator"

    """Table Simulator the tva """
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Simulator_Advertiser', on_delete=models.CASCADE,
                                   null=True)
    scenario_name = models.CharField(max_length=50, blank=True)
    scenario_info = models.TextField(blank = True)
    date_time = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.scenario_name

    def get_date_time(self):
        date_time = datetime.datetime.strptime(str(self.date_time).replace('/', '-')[:19], '%Y-%m-%d %H:%M:%S')
        return date_time.strftime('%Y-%m-%d %H:%M:%S')


class ImportFile(models.Model):

    class Meta:
        verbose_name_plural = "System ImportFile"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='ImportFile_Advertiser', on_delete=models.CASCADE,
                                   null=True)
    date_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    name_file = models.TextField(blank = True)
    campaign = models.ForeignKey('Campaign', related_name='ImportFile_Campaign', on_delete=models.SET_NULL, null=True)
    campaign_name = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=100, blank=True)
    module = models.CharField(max_length=100, blank=True)
    module_name = models.ForeignKey('TvaModule', related_name='ImportFile_TvaModule', on_delete=models.SET_NULL,
                               null=True)
    start_time = models.DateTimeField(blank=True, editable=True)
    end_time = models.DateTimeField(blank=True, editable=True)
    log_info = models.TextField(blank=True)

    @property
    def get_advertiser_name(self):
        if self.advertiser is not None:
            return self.advertiser.name
        else:
            return 'Unknown'


class ConfigruationAdvertiser(models.Model):

    class Meta:
        verbose_name_plural = "System Configruation Advertiser"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    enabled = models.BooleanField(default=False)
    advertiser = models.ForeignKey('Advertiser', related_name='ConfigruationAdvertiser_Advertiser', on_delete=models.CASCADE,
                                   null=True)
    name_configuration = models.CharField(max_length=100, blank=False)
    date_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    date_time_update = models.DateTimeField(default=datetime.datetime.now, blank=True)
    configuration = models.TextField(blank = False)

    @property
    def get_advertiser_name(self):
        return self.advertiser.name


class SystemConfig(models.Model):

    class Meta:
        verbose_name_plural = "System Config"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    type_config = models.CharField(max_length=100, blank=False)
    name_configuration = models.CharField(max_length=100, blank=False)
    date_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    date_time_update = models.DateTimeField(default=datetime.datetime.now, blank=True)
    configuration = models.TextField(blank = False)

    @property
    def get_name_configuration(self):
        return self.name_configuration

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Media(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Media"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Media_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Media_Campaign', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class FeatureType(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Feature Type"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='FeatureType_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='FeatureType_Campaign', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class Feature(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Feature"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Feature_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Feature_Campaign', on_delete=models.CASCADE, null=True)
    feature_type = models.ForeignKey('FeatureType', related_name='Feature_FeatureType',
                                   on_delete=models.CASCADE,
                                   null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    log = models.ForeignKey('ImportFile', related_name='Feature_ImportFile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Betas(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Betas"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Betas_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Betas_Campaign', on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey('Feature', related_name='Betas_Feature',
                                     on_delete=models.CASCADE,
                                     null=True)
    beta = models.FloatField(default=0, blank=True, help_text="Beta")
    pvalue = models.FloatField(default=0, blank=True, help_text="Pvalue")
    log = models.ForeignKey('ImportFile', related_name='Betas_ImportFile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.feature.name

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Alphas(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Alphas"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Alphas_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Alphas_Campaign', on_delete=models.CASCADE, null=True)
    media = models.ForeignKey('Media', related_name='Alphas_Media',
                                     on_delete=models.CASCADE,
                                     null=True)
    alpha = models.FloatField(default=0, blank=True, help_text="alpha")
    log = models.ForeignKey('ImportFile', related_name='Alphas_ImportFile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.media.name

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Sales(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Sales"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Sales_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Sales_Campaign', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Start Date")
    sale = models.FloatField(default=0, blank=True, help_text="sale")
    log = models.ForeignKey('ImportFile', related_name='Sales_ImportFile', on_delete=models.CASCADE, null=True)


    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class ValuesForcasted(models.Model):
    class Meta:
        verbose_name_plural = "Media-Mix Values Forcasted"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='ValuesForcasted_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='ValuesForcasted_Campaign', on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey('Feature', related_name='ValuesForcasted_Feature',
                                on_delete=models.CASCADE,
                                null=True)
    feature_type = models.ForeignKey('FeatureType', related_name='ValuesForcasted_FeatureType',
                                     on_delete=models.CASCADE,
                                     null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Start Date")
    week_month = models.IntegerField(default=0, help_text="week of month")

    inv_original = models.FloatField(default=0, blank=True, help_text="Inv Original")
    value = models.FloatField(default=0, blank=True, help_text="Value")
    sale_forecasted = models.FloatField(default=0, blank=True, help_text="Sale_Forecasted")
    log = models.ForeignKey('ImportFile', related_name='ValuesForcasted_ImportFile', on_delete=models.CASCADE, null=True)


    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class AdsTocks(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix AdStocks"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Adstocks_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='AdsTocks_Campaign', on_delete=models.CASCADE, null=True)
    media = models.ForeignKey('Media', related_name='Adstocks_Media',
                                     on_delete=models.CASCADE,
                                     null=True)
    dragged_adstocks = models.FloatField(default=0, blank=True, help_text="Dragged Adstocks")
    original_adstocks = models.FloatField(default=0, blank=True, help_text="Original Adstocks")
    original_investment = models.FloatField(default=0, blank=True, help_text="Original investment")
    calculated_adstocks = models.FloatField(default=0, blank=True, help_text="Calculated Adstocks")
    log = models.ForeignKey('ImportFile', related_name='AdsTocks_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class SimulatorCalculator(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Simulator Calculator"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='SimulatorCalculator_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='SimulatorCalculator_Campaign', on_delete=models.CASCADE, null=True)
    item = models.CharField(max_length=250)
    edit = models.BooleanField(default=False)
    hitorical = models.FloatField(default=0, blank=True, help_text="Historical")

    beta = models.FloatField(default=0, blank=True, help_text="Beta")
    forcasted = models.FloatField(default=0, blank=True, help_text="forcasted")
    forcasted_sales_feature = models.FloatField(default=0, blank=True, help_text="Forcasted sales feature")
    log = models.ForeignKey('ImportFile', related_name='SimulatorCalculator_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Constants(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Constants"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Constants_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Constants_Campaign', on_delete=models.CASCADE, null=True)
    constant = models.CharField(max_length=100)
    value = models.FloatField(default=0, blank=True, help_text="Value")
    log = models.ForeignKey('ImportFile', related_name='Constants_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class MixSalesEvolution(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix MixSales Evolution"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='MixSalesEvolution_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MixSalesEvolutionCampaign', on_delete=models.CASCADE, null=True)
    media = models.ForeignKey('Media', related_name='MixSalesEvolution_Media',
                              on_delete=models.CASCADE,
                              null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    value = models.FloatField(default=0, blank=True, help_text="value")
    log = models.ForeignKey('ImportFile', related_name='MixSalesEvolution_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class CostPerUnitSoldRoas(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix CostPerUnitSoldRoas"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='CostPerUnitSoldRoas_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='CostPerUnitSoldRoas_Campaign', on_delete=models.CASCADE, null=True)
    media = models.ForeignKey('Media', related_name='CostPerUnitSoldRoas_Media',
                              on_delete=models.CASCADE,
                              null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    cost_per_unit_sold = models.FloatField(default=0, blank=True, help_text="Cost per unit_sold")
    roas = models.FloatField(default=0, blank=True, help_text="Roas")
    log = models.ForeignKey('ImportFile', related_name='CostPerUnitSoldRoas_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Seasonality(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Seasonality"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Seasonality_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Seasonality_Campaign', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    baseline_value = models.FloatField(default=0, blank=True, help_text="baseline value")
    seasonality_value = models.FloatField(default=0, blank=True, help_text="seasonality value")
    log = models.ForeignKey('ImportFile', related_name='Seasonality_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Competition(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Competition"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Competition_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Competition_Campaign', on_delete=models.CASCADE, null=True)
    feature = models.ForeignKey('Feature', related_name='Competition_Feature',
                                     on_delete=models.CASCADE,
                                     null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    value = models.FloatField(default=0, blank=True, help_text="Value")


class Precition(models.Model):

    class Meta:
        verbose_name_plural = "Media-Mix Precition"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='Precition_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='Precition_Campaign', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    reale_sales = models.FloatField(default=0, blank=True, help_text="Reale sales")
    forcasted_sales = models.FloatField(default=0, blank=True, help_text="forcasted_sales")
    log = models.ForeignKey('ImportFile', related_name='Precition_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class ConversionType(models.Model):

    class Meta:
        verbose_name_plural = "MTA ConversionType"
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='ConversionType_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='ConversionType_Campaign', on_delete=models.CASCADE, null=True)
    conversion_type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)


class MtaResult(models.Model):
    class Meta:
        verbose_name_plural = "MTA Result"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='MtaResult_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MtaResult_Campaign', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    conversion_type = models.ForeignKey('ConversionType', related_name='MtaResult_conversionType', on_delete=models.CASCADE, null=True)
    channel = models.ForeignKey('Chanel', related_name='MtaResult_chanel', on_delete=models.CASCADE, null=True)
    revenue_shapley = models.FloatField(default=0, blank=True, help_text="Revenue shapley")
    atributed_conversion_shapley = models.FloatField(default=0, blank=True, help_text="Atributed Conversion Shapley")
    atributed_conversiones_lineal = models.FloatField(default=0, blank=True, help_text="Atributed Conversiones Lineal")
    revenue_linear = models.FloatField(default=0, blank=True, help_text="Revenue Linear")
    revenue_first_click = models.FloatField(default=0, blank=True, help_text="Revenue_Frst Click")
    revenue_last_click = models.FloatField(default=0, blank=True, help_text="Revenue Last Click")
    stimuli_quantity_paths = models.FloatField(default=0, blank=True, help_text="Stimuli Quantity Paths")
    paths_quantity = models.FloatField(default=0, blank=True, help_text="Paths Quantity")
    assistances_role = models.FloatField(default=0, blank=True, help_text="Rol assistances (of the paths ending today)")
    conversion_role = models.FloatField(default=0, blank=True, help_text="Role conversion (of the paths ending today)")
    acquisition_role = models.FloatField(default=0, blank=True, help_text="Acquisition role(of the paths ending today)")
    shapley = models.FloatField(default=0, blank=True, help_text="Shapley")
    this_type_conversions = models.FloatField(default=0, blank=True, help_text="This type conversions")
    convertion_paths_with_this_channel = models.FloatField(default=0, blank=True, help_text="Convertion paths with this channel")
    daily_impulses = models.FloatField(default=0, blank=True, help_text="Daily impulses")
    campaign_mta = models.CharField(max_length=300,default='')
    source = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=100, default='')
    log = models.ForeignKey('ImportFile', related_name='MtaResult_ImportFile', on_delete=models.CASCADE, null=True)

    @property
    def get_log(self):
        if not self.log:
            return 'Unknow'
        else:
            return self.log.name_file


class Invesment(models.Model):

    class Meta:
        verbose_name_plural = "MTA Invesment"

    date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    advertiser = models.ForeignKey('Advertiser', related_name='MtaInvesment_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTAInvesment_Campaign', on_delete=models.CASCADE, null=True)
    channel = models.ForeignKey('Chanel', related_name='MTAInvesment_chanel', on_delete=models.CASCADE, null=True)
    invesment = models.FloatField(default=0, blank=True, help_text="invesment")
    campaign_mta = models.CharField(max_length=100, default='')
    source = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=100, default='')
    log = models.ForeignKey('ImportFile', related_name='Invesment_ImportFile', on_delete=models.CASCADE,
                            null=True)


class PathsMetrics(models.Model):

    class Meta:
        verbose_name_plural = "MTA PathsMetrics"

    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    advertiser = models.ForeignKey('Advertiser', related_name='MTAPathsMetrics_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTAPathsMetrics_Campaign', on_delete=models.CASCADE, null=True)
    total_paths = models.FloatField(default=0, blank=True, help_text="total_paths")
    log = models.ForeignKey('ImportFile', related_name='MTAPathsMetrics_ImportFile', on_delete=models.CASCADE, null=True)


class PathAnalisisTouchpoint(models.Model):

    class Meta:
        verbose_name_plural = "MTA PathAnalisisTouchpoint"

    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    advertiser = models.ForeignKey('Advertiser', related_name='MTAPathAnalisisTouchpoint_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTAPathAnalisisTouchpoint_Campaign', on_delete=models.CASCADE, null=True)
    conversion_type = models.ForeignKey('ConversionType', related_name='MtaPathAnalisisTouchpoint_conversionType',
                                        on_delete=models.CASCADE, null=True)
    touchpoints_quantity = models.FloatField(default=0, blank=True, help_text="total_paths")
    paths_count = models.FloatField(default=0, blank=True, help_text="total_paths")
    log = models.ForeignKey('ImportFile', related_name='MTAPathAnalisisTouchpoint_ImportFile', on_delete=models.CASCADE, null=True)


class PathAnalisisChannels(models.Model):

    class Meta:
        verbose_name_plural = "MTA PathAnalisisChannels"

    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    advertiser = models.ForeignKey('Advertiser', related_name='MTAPathAnalisisChannels_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTAPathAnalisisChannels_Campaign', on_delete=models.CASCADE, null=True)
    conversion_type = models.ForeignKey('ConversionType', related_name='MtaPathAnalisisChannels_conversionType',
                                        on_delete=models.CASCADE, null=True)
    channels_quantity = models.FloatField(default=0, blank=True, help_text="total_paths")
    paths_count = models.FloatField(default=0, blank=True, help_text="total_paths")
    log = models.ForeignKey('ImportFile', related_name='MTAPathAnalisisChannels_ImportFile', on_delete=models.CASCADE, null=True)


class CoalitionsMetrics(models.Model):

    class Meta:
        verbose_name_plural = "MTA CoalitionsMetrics"

    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    advertiser = models.ForeignKey('Advertiser', related_name='MTACoalitionsMetrics_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTACoalitionsMetrics_Campaign', on_delete=models.CASCADE, null=True)
    channel = models.ForeignKey('Chanel', related_name='MTACoalitionsMetrics_chanel', on_delete=models.CASCADE, null=True)
    coalitions = models.CharField(max_length=200)
    len_coalitions = models.IntegerField(default=0, help_text="Len Coalitions")
    total_paths = models.FloatField(default=0, blank=True, help_text="total")
    conversion_paths = models.FloatField(default=0, blank=True, help_text="conversion_paths")
    conversion_rate = models.FloatField(default=0, blank=True, help_text="conversion_rate")
    channel_attribution = models.FloatField(default=0, blank=True, help_text="channel_attribution")
    log = models.ForeignKey('ImportFile', related_name='MTACoalitionsMetrics_ImportFile', on_delete=models.CASCADE, null=True)


class Irma(models.Model):

    class Meta:
        verbose_name_plural = "MTA Irma"

    date = models.DateTimeField(blank=False, editable=True, help_text="Date")
    advertiser = models.ForeignKey('Advertiser', related_name='MTAIrma_Advertiser',
                                   on_delete=models.CASCADE,
                                   null=True)
    campaign = models.ForeignKey('Campaign', related_name='MTAIrma_Campaign', on_delete=models.CASCADE, null=True)
    len_coalitions = models.IntegerField(default=0, help_text="Len coalitions")
    coalitions = models.FloatField(default=0, blank=True, help_text="coalitions")
    conversion_volume = models.FloatField(default=0, blank=True, help_text="conversion_volume")
    conversion_percentage = models.FloatField(default=0, blank=True, help_text="conversion_percentage")
    possible_truncation = models.FloatField(default=0, blank=True, help_text="Possible truncation")
    zero_percentage = models.FloatField(default=0, help_text="zero_percentage")
    zero_ten_percentage = models.FloatField(default=0, help_text="zero_ten_percentage")
    ten_twenty_percentage = models.FloatField(default=0, help_text="ten_twenty_percentage")
    twenty_thirty_percentage = models.FloatField(default=0, help_text="twenty_thirty_percentage")
    thirty_fourty_percentage = models.FloatField(default=0, help_text="thirty_fourty_percentage")
    fourty_fifty_percentage = models.FloatField(default=0, help_text="fourty_fifty_percentage")
    fifty_sixty_percentage = models.FloatField(default=0, help_text="fifty_sixty_percentage")
    sixty_seventy_percentage = models.FloatField(default=0, help_text="sixty_seventy_percentage")
    seventy_eighty_percentage = models.FloatField(default=0, help_text="seventy_eighty_percentage")
    eighty_ninety_percentage = models.FloatField(default=0, help_text="eighty_ninety_percentage")
    ninety_onehundred_percentage = models.FloatField(default=0, help_text="ninety_onehundred_percentage")
    one_hundred_percentage = models.FloatField(default=0, help_text="one_hundred_percentage")
    total = models.FloatField(default=0, help_text="total")
    log = models.ForeignKey('ImportFile', related_name='MTAMTAIrma_ImportFile', on_delete=models.CASCADE, null=True)


class DataStudioWorkSpace(models.Model, WorkSpace):
    class Meta:
        verbose_name_plural = "Data Studio WorkSpace"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    work_space = models.CharField(max_length=50, blank=True)
    name_work_space = models.CharField(max_length=50, blank=True)
    id_work_space_ds = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name_work_space

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class UserDataStudio(models.Model):
    class Meta:
        verbose_name_plural = "Data Studio User"

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_studio_work_space = models.ManyToManyField(DataStudioWorkSpace, related_name='UserDataStudio_DataStudioWorkSpace',
                                                blank=True)

    def __str__(self):
        return ''

    def get_list_work_space_id(self, obj=None):
        list_work_space = self.data_studio_work_space.values_list('id')
        return list_work_space


class DataStudoMenu(models.Model):
    class Meta:
        verbose_name_plural = "Data Studio Menu"

    enabled = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='DataStudoMenu_advertiser', on_delete=models.CASCADE,
                                   null=True)
    work_spaces = models.ForeignKey('DataStudioWorkSpace', related_name='DataStudoMenu_DataStudioWorkSpace',
                                    on_delete=models.CASCADE,
                                    null=True)
    id_report = models.CharField(max_length=50, blank=True, default='')
    name = models.CharField(max_length=50, blank=True)
    menu = models.CharField(max_length=50, blank=True)
    url_report  = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    order_menu = models.IntegerField(default=0, help_text="Order Menu")

    def __str__(self):
        return self.name

    def get_work_spaces(self):
        return self.work_spaces.work_space

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class AdvertirserInsights(models.Model):

    class Meta:
        verbose_name_plural = "System Advertirser Insights"

    enabled = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True, help_text="Unique id")
    advertiser = models.ForeignKey('Advertiser', related_name='AdvertirserInsights_advertiser',
                                   on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey('Campaign', related_name='AdvertirserInsights_Campaign', on_delete=models.CASCADE, null=True)
    module = models.ForeignKey('TvaModule', related_name='AdvertirserInsights_TvaModule', on_delete=models.CASCADE,
                               null=True)
    menu = models.CharField(max_length=50, blank=True)
    sub_menu = models.CharField(max_length=50, blank=True)

    insights = models.TextField(blank=True)

    def __str__(self):
        return self.insights


class UploadFilesModule(models.Model):

    class Meta:
        verbose_name_plural = "System Upload Files Module"

    id = models.AutoField(primary_key=True, help_text="Unique id")
    file_name = models.CharField(max_length=250, blank=True)
    advertiser = models.ForeignKey('Advertiser', related_name='UploadFilesModule_advertiser',
                                   on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey('Campaign', related_name='UploadFilesModule_Campaign', on_delete=models.CASCADE, null=True)
    module = models.ForeignKey('TvaModule', related_name='UploadFilesModule_TvaModule', on_delete=models.CASCADE,
                               null=True)
    description = models.TextField(blank=True)
    url_file = models.CharField(max_length=250, blank=True)
    date_time = models.DateTimeField(default=datetime.datetime.now, blank=True)
    status = models.BooleanField(default=False)
    log = models.ForeignKey('ImportFile', related_name='UploadFilesModule_ImportFile', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.file_name

    def log_id(self):
        print(self.log)
        if self.log:
            return self.log.id
        else:
            return -1


