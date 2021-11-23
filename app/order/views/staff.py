import csv
from datetime import date

from django.contrib import messages
from django.shortcuts import render

from core.decorators import staff_login_required
from core.paginator import paginate_query
from order.forms import OrderSearchForm
from order.models import Sales, SalesDetails


@staff_login_required
def order_info(request):
    """ 注文情報（スタッフ）

    :param request:
    :return:
    """
    search_form = OrderSearchForm(request.GET)
    qs = Sales.objects.none()

    if 'created_at_from' in request.GET or 'created_at_to' in request.GET:
        # 検索
        if search_form.is_valid():
            cleaned_data = search_form.cleaned_data
            qs = Sales.objects.all()
            # 注文日 from
            if cleaned_data['created_at_from']:
                qs = qs.filter(created_at__gte=cleaned_data['created_at_from'])
            # 注文日 to
            if cleaned_data['created_at_to']:
                qs = qs.filter(created_at__lte=cleaned_data['created_at_to'])

    page_obj = paginate_query(request, qs)

    # 注文情報ダウンロード
    if request.method == 'POST':

        sales_id_list = qs.values_list('pk', flat=True)
        order_list = SalesDetails.objects.filter(sales_id__in=sales_id_list)

        t = date.today()
        output_path = '/var/www/d_shopping/app/download/'
        output_name = t.strftime('%Y%m') + '_billing.csv'

        # CSV出力処理開始
        with open(output_path + output_name, 'w', encoding='cp932', newline='') as csv_file:
            # 1行目にヘッダーを書き込む
            header = ['受注日時', '顧客名', '電話番号', '商品名', '数量', '価格']
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            writer.writerow(header)

            for order in order_list:
                order_date = order.sales.created_at
                customer = order.sales.name
                phone_number = order.sales.phone_number
                product_name = order.product.name
                quantity = order.quantity
                price = order.price

                row = []
                row += [order_date, customer, phone_number, product_name, quantity, price]

                writer.writerow(row)

        messages.success(request, '/var/www/d_shopping/app/download/にファイルをダウンロードしました。')

    return render(
        request,
        'order_info/order_info.html',
        context={
            'page_obj': page_obj,
            'search_form': search_form,
        }
    )
