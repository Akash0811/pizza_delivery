from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    """A new order for the user"""
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey( User , on_delete=models.CASCADE )
    price = models.FloatField( default = 0.0 )
    buy = models.BooleanField( default = False)
    time = now()

class TemplateNonSizableDish(models.Model):
    """ A dish that has no size """
    name = models.CharField(max_length=64)
    SmallPrice = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} - {self.SmallPrice}"

    class Meta:
        abstract = True

class TemplateTopping(models.Model):
    """ A Topping to be added on the dish """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        abstract = True

class TemplateSizableDish(TemplateNonSizableDish):
    """ A dish that has a size """
    LargePrice = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice}"

    class Meta:
        abstract = True

'''templates contain pice of items to be shown on menu
Admin can change prices dynamically
Required because cannot have same database for templates and orders'''

class TemplateRegularPizza(TemplateSizableDish):
    Topping1SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping2SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping3SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping1LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping2LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping3LargePrice = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

class TemplateSicilianPizza(TemplateSizableDish):
    Topping1SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping2SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping3SmallPrice = models.FloatField(null=True, blank=True, default=None)
    Topping1LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping2LargePrice = models.FloatField(null=True, blank=True, default=None)
    Topping3LargePrice = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

class TemplateSub(TemplateSizableDish):
    XCheesePrice = models.FloatField(null=True, blank=True, default=0.50)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

    class Meta:
        abstract = True

class TemplateDPS(TemplateSizableDish):
    def price(self):
        return self.SmallPrice

    class Meta:
        abstract = True

    pass

class TemplatePS(TemplateNonSizableDish):
    class Meta:
        abstract = True
    pass


'''Real orders are passed and hence these are linked to attributes and orders databases
This is displayed on cart , not on menu
'''

class Topping(TemplateTopping):
    id = models.BigAutoField(primary_key=True)
    pass

class RegularPizza(TemplateRegularPizza):
    id = models.BigAutoField(primary_key=True)
    size = models.BooleanField(default = False)
    orders = models.ManyToManyField(Order, blank=True, related_name="regular_dish")
    toppings = models.ManyToManyField(Topping, blank=True, related_name="regular_dish")
    no_of_toppings = models.IntegerField( default = 0 )

    def price(self):
        if self.size == False:
            if self.no_of_toppings == 1:
                return self.Topping1SmallPrice
            elif self.no_of_toppings == 2:
                return self.Topping2SmallPrice
            elif self.no_of_toppings >= 3:
                return self.Topping3SmallPrice
            else:
                return self.SmallPrice
        else:
            if self.no_of_toppings == 1:
                return self.Topping1LargePrice
            elif self.no_of_toppings == 2:
                return self.Topping2LargePrice
            elif self.no_of_toppings >= 3:
                return self.Topping3LargePrice
            else:
                return self.LargePrice


class SicilianPizza(TemplateSicilianPizza):
    id = models.BigAutoField(primary_key=True)
    orders = models.ManyToManyField(Order, blank=True, related_name="sicilian_dish")
    size = models.BooleanField(default = False)
    toppings = models.ManyToManyField(Topping, blank=True, related_name="sicilian_dish")
    no_of_toppings = models.IntegerField( default = 0 )

    def price(self):
        if self.size == False:
            if self.no_of_toppings == 1:
                return self.Topping1SmallPrice
            elif self.no_of_toppings == 2:
                return self.Topping2SmallPrice
            elif self.no_of_toppings >= 3:
                return self.Topping3SmallPrice
            else:
                return self.SmallPrice
        else:
            if self.no_of_toppings == 1:
                return self.Topping1LargePrice
            elif self.no_of_toppings == 2:
                return self.Topping2LargePrice
            elif self.no_of_toppings >= 3:
                return self.Topping3LargePrice
            else:
                return self.LargePrice

class Sub(TemplateSub):
    id = models.BigAutoField(primary_key=True)
    size = models.BooleanField(default = False)
    orders = models.ManyToManyField(Order, blank=True, related_name="subs0_dish")
    Xcheese = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} - Small:{self.SmallPrice} - Large:{self.LargePrice} - ExtraCheese:{self.XCheesePrice}"

    def price(self):
        if self.size == False:
            if self.Xcheese == False:
                return self.SmallPrice
            else:
                return self.SmallPrice + self.XCheesePrice
        else:
            if self.Xcheese == False:
                return self.LargePrice
            else:
                return self.LargePrice + self.XCheesePrice

class DinnerPlatter(TemplateDPS):
    id = models.BigAutoField(primary_key=True)
    size = models.BooleanField(default = False)
    orders = models.ManyToManyField(Order, blank=True, related_name="dinnerplatter_dish")
    pass
    
class Pasta(TemplatePS):
    id = models.BigAutoField(primary_key=True)
    orders = models.ManyToManyField(Order, blank=True, related_name="pasta_dish")
    pass

class Salad(TemplatePS):
    id = models.BigAutoField(primary_key=True)
    orders = models.ManyToManyField(Order, blank=True, related_name="salad_dish")
    pass

class DisplayRegularPizza(TemplateRegularPizza):
    '''Display of Regular Pizzas on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

class DisplaySicilianPizza(TemplateSicilianPizza):
    '''Display of Sicilian Pizzas on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

class DisplaySub(TemplateSub):
    '''Display of Subs on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

class DisplayDinnerPlatter(TemplateDPS):
    '''Display of Dinner Platter on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

class DisplayPasta(TemplateDPS):
    '''Display of Pasta on Menu''' 
    id = models.BigAutoField(primary_key=True)
    pass

class DisplaySalad(TemplateDPS):
    '''Display of Salad on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

class DisplayTopping(TemplateTopping):
    '''Display of Salad on Menu'''
    id = models.BigAutoField(primary_key=True)
    pass

