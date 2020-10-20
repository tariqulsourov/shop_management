from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .models import Brand, ProductType, Products
from .forms import ProductForm, BrandForm, ProductTypeForm

from xlrd import open_workbook
import os
import shutil
import barcode
from barcode.writer import ImageWriter

def home(request):

    return render(request, 'home.html', context={})

def productList(request):
    all_product = Products.objects.all()
    print('abcd')
    
    return render(request, 'product/all_products.html', {'all_products' : all_product})

def addProduct(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    # print(context['form'])
    return render(request, 'product/product_form.html', context)

def addBrand(request):
    form = BrandForm(request.POST)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'product/brand_form.html', context)


def addType(request):
    form = ProductTypeForm(request.POST)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'product/ptoduct_type_form.html', context)


def addProductFromExcel(request):
    if request.method == 'GET':
        get_type = ProductType.objects.all()
        return render(request, 'product/add_from_excel.html', {'get_type':get_type})
    if request.method == 'POST' and request.FILES['xlFile']:
        products_type = request.POST.get('type')
        xlFile = request.FILES['xlFile']
        fs = FileSystemStorage()
        file_name = fs.save(xlFile.name, xlFile)
        file_size = fs.size(xlFile.name)
        # print(products_type)
        # print(file_size)

        file_path = 'media/'+file_name
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_dir = os.path.join(BASE_DIR, file_path)
        # print(file_dir)
        items = []

        rows = []
        
        wb = open_workbook(file_dir)
        for sheet in wb.sheets():
            number_of_rows = sheet.nrows
            print(number_of_rows)

            number_of_columns = sheet.ncols
            # print(number_of_columns)

            
            for row in range(0, number_of_rows):
                values = []
                for col in range(0, number_of_columns):
                    value  = (sheet.cell(row,col).value)
                    # print('-----------------')
                    # print(value)
                    try:
                        value = str(value)
                        # print(value)
                        values.append(value)
                    except ValueError:
                        pass
                # item = Arm(*values)
                # print(values)
                items.append(values)
        p_type = ProductType.objects.get(id = products_type)
        # print(type(p_type))
        for item in items:
            p_name= item[1]
            p_description= item[3]
            p_image= item[4]
            p_volume= item[5]
            p_buying_price= int(float(item[6]))
            p_available_quantity= int(float(item[7]))
            p_selling_price = (p_buying_price*.2)+p_buying_price

            p_bar_code= str(p_type)+p_name+p_volume.replace(' ','')+str(p_buying_price)
            print(p_bar_code)

            bar_class = barcode.get_barcode_class('code39')
            bar_code = bar_class(p_bar_code, writer = ImageWriter())
            bar_img = bar_code.save(p_bar_code)

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            source_dir = os.path.join(BASE_DIR, bar_img)
            destination_dir = os.path.join(BASE_DIR, 'static/images')
            shutil.move(source_dir, destination_dir)

            single_product = Products(name = p_name, description= p_description,
                                    p_image = p_image, volume_weight = p_volume,
                                    buying_price = p_buying_price, available_quantity = p_available_quantity,
                                    bar_code = p_bar_code, bar_code_image = bar_img,
                                    selling_price = p_selling_price, brand_id = 1, p_type_id = products_type)
                
            single_product.save()

        return redirect('add-excel')

# def generateBarcode(request):
#     bar_class = barcode.get_barcode_class('code39')
#     bar_code = bar_class('abc123', writer = ImageWriter())
#     bar_img = bar_code.save('test')
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     print(BASE_DIR)
#     return render(request, 'product/barcode.html', {'bar_img':bar_img})