
import pandas as pd
from dotenv import load_dotenv


from client import ShimokuClient
from recycler.recycler_reporter import RecyclerReporter


def run():
    df1 = pd.read_csv('recycler/sales.csv')
    df2 = pd.read_csv('recycler/users.csv')
    df = pd.merge(df1, df2, on='client_id', how='inner', suffixes=('', '_user'))
    reporter = RecyclerReporter(df)
    s = ShimokuClient()
    s.create_dashboard('Recycler')
    menu_path = 'recycler'
    s.delete_app(menu_path)
    order = 0

    s.client.plt.html(
        html=s.client.html_components.beautiful_indicator(
            title="Recycler main dashboard",
            href="https://shimoku.io/f4fd08a3-bea2-4b77-90a3-de2b52e8ab74/usuarios-activos-mensuales",
            background_url="https://images.unsplash.com/photo-1628771065518-0d82f1938462",
        ),
        menu_path=menu_path,
        order=order,
        rows_size=1,
        cols_size=12,
    )
    order += 1

    data = [
        {
            "variant": "outlined",
            "description": pd.to_datetime('today').month_name(),
            "title": "Productos vendidos en el mes",
            "align": "left",
            "value": reporter.sold_products_by_month().tail(1).values[0][1],
        },
        {
            "color": "success" if reporter.recycled_products_percentage_by_month() > 50 else "caution",
            "variant": "contained",
            "description":  pd.to_datetime('today').month_name(),
            "title": "Productos reciclados",
            "align": "left",
            "value": reporter.recycled_products_by_month().tail(1).values[0][1],
        },
        {
            "color": "success" if reporter.recycled_products_percentage_by_month() > 50 else "caution",
            "variant": "contained",
            "description": pd.to_datetime('today').month_name(),
            "title": "Porcentaje de productos reciclados",
            "align": "left",
            "value": f"{reporter.recycled_products_percentage_by_month()}%",
        },
    ]
    s.client.plt.indicator(
        data=data,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=3,
        value='value',
        header='title',
        footer='description',
        color='color',
        variant='variant',
        vertical=True
    )
    order += 3

    data = reporter.sales_with_problems()
    s.client.plt.table(
        data=data[['client_id','ticket_id']].tail(5),
        menu_path=menu_path,
        order=order,
        cols_size=4,
        rows_size=2,
        title='Lista ventas con incidencias en este mes',
    )
    order += 1

    s.client.plt.radar(
        data=reporter.gender_comparative(),
        x='gender', y=reporter.gender_comparative().drop('gender', axis=1).columns.tolist(),
        menu_path=menu_path,
        order=order, rows_size=3, cols_size=5,
        title='Comparativa entre géneros',
    )
    order += 1

    s.client.plt.update_tabs_group_metadata(
        menu_path=menu_path,
        group_name='evolution',
        order=order,
        sticky=False,
        just_labels=False,
        rows_size=0,
    )
    order += 1

    s.client.plt.line(
        data=reporter.month_comparative(),
        menu_path=menu_path, order=order,
        x='mes', y=['productos_vendidos', 'recycled_qt', 'anomalías', 'non_recycled_qt'],
        rows_size=2, cols_size=12,
        title='Usuarios únicos mensuales',
        tabs_index=("evolution", "Crecimiento mensual")
    )
    order += 1

    s.client.plt.stacked_barchart(
        data=reporter.month_sells_comparative_by_brand().tail(12).reset_index(drop=True),
        menu_path=menu_path,
        order=order,
        x="mes",
        x_axis_name='Mes de la compra',
        rows_size=3, cols_size=12,
        subtitle='Comparativa de ventas por marca',
        tabs_index=("evolution", "Ventas por marca")
    )
    order += 1

    s.client.plt.stacked_barchart(
        data=reporter.month_sells_comparative_by_platform().tail(12),
        menu_path=menu_path,
        order=order,
        x="mes",
        x_axis_name='Mes de la compra',
        rows_size=3, cols_size=12,
        subtitle='Comparativa de ventas por marca',
        tabs_index=("evolution", "Ventas por plataforma")
    )
    order += 1


    html = (
        "<p>Comparativa de ventas del ultimo mes por marca</p>"
    )
    s.client.plt.html(
        html=html,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=6,
    )
    order += 1

    html = (
        "<p>Comparativa de ventas del ultimo mes por plataforma</p>"
    )
    s.client.plt.html(
        html=html,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=6,
    )
    order += 1

    s.client.plt.rose(
        data=reporter.month_sells_comparative_by_brand().tail(1).drop('mes', axis=1).melt(var_name='name', value_name='value'),
        menu_path=menu_path,
        order=order,
        cols_size=6,
        rows_size=2,
    )
    order += 1

    s.client.plt.doughnut(
        data=reporter.month_sells_comparative_by_platform().tail(1).drop('mes', axis=1).melt(var_name='name', value_name='value'),
        menu_path=menu_path,
        order=order,
        cols_size=6,
        rows_size=2
    )
    order += 1

    html = (
        "<p>Comparativa de reciclajes del ultimo mes por marca</p>"
    )
    s.client.plt.html(
        html=html,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=6,
    )
    order += 1

    html = (
        "<p>Comparativa de reciclajes del ultimo mes por plataforma</p>"
    )
    s.client.plt.html(
        html=html,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=6,
    )
    order += 1

    s.client.plt.rose(
        data=reporter.month_recycle_comparative_by_brand().tail(1).drop('mes', axis=1).melt(var_name='name', value_name='value'),
        menu_path=menu_path,
        order=order,
        cols_size=6,
        rows_size=2
    )
    order += 1

    s.client.plt.doughnut(
        data=reporter.month_recycle_comparative_by_platform().tail(1).drop('mes', axis=1).melt(var_name='name', value_name='value'),
        menu_path=menu_path,
        order=order,
        cols_size=6,
        rows_size=2
    )
    order += 1


    html = (
        "<p>Lista de ventas con incidences</p>"
    )
    s.client.plt.html(
        html=html,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=12,
    )
    order += 1
    s.client.plt.table(
        data=reporter.sales_with_problems()[['client_id', 'ticket_id', 'created_at', 'cantidad', 'points_used', 'recycled_platform']],
        menu_path=menu_path,
        order=order,
        cols_size=12,
        rows_size=2,
    )
    return s


if __name__ == '__main__':
    load_dotenv()
    s = run()

    s.client.activate_async_execution()
    s.client.run()
