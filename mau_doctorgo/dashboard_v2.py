import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from client import ShimokuClient
from mau_doctorgo.mau_reporter import MauReporter


def run():
    df = pd.read_csv('mau_doctorgo/data.csv')
    reporter = MauReporter(df)

    s = ShimokuClient()
    s.create_dashboard(os.getenv('DASHBOARD_NAME'))
    menu_path = 'Usuarios activos mensuales v2'
    s.delete_app(menu_path)
    order = 0

    s.client.plt.html(
        html=s.client.html_components.beautiful_indicator(
            title="Usuarios Mensuales Activos UMA V2",
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
            "description": "",
            "title": "Usuarios activos totales",
            "align": "right",
            "value": reporter.unique_au_quantity(),
        },
        {
            "variant": "outlined",
            "description": (pd.to_datetime('today') - pd.DateOffset(months=1)).month_name(),
            "title": "Usuarios activos en el mes anterior",
            "align": "right",
            "value": reporter.unique_mau_quantity_previous_month(),
        },
        {
            "color": "success" if reporter.unique_mau_quantity_current_month() > reporter.unique_mau_quantity_previous_month() else "caution",
            "variant": "contained",
            "description": pd.to_datetime('today').month_name(),
            "title": "Usuarios activos en el mes actual",
            "align": "right",
            "value": reporter.unique_mau_quantity_current_month(),
        }
    ]
    s.client.plt.indicator(
        data=data,
        menu_path=menu_path,
        order=order, rows_size=1, cols_size=12,
        value='value',
        header='title',
        footer='description',
        color='color',
        variant='variant',
    )
    order += 3

    data = reporter.unique_mau_quantity()
    data['fecha_alta'] = data['fecha_alta'].astype(str)

    s.client.plt.update_tabs_group_metadata(
        menu_path=menu_path,
        group_name='MAU_qt',
        order=order,
        sticky=False,
        just_labels=True,
        rows_size=0,
    )
    order += 1

    s.client.plt.line(
        data=data,
        menu_path=menu_path, order=order,
        x='fecha_alta', y=['cantidad'],
        rows_size=2, cols_size=12,
        title='Usuarios únicos mensuales',
        tabs_index=("MAU_qt", "crecimiento mensual")
    )
    order += 1

    data = reporter.unique_mau_quantity_yearly()
    s.client.plt.line(
        data=data,
        menu_path=menu_path, order=order,
        x='Mes', y=data.columns.drop(['Mes']).tolist(),
        rows_size=2, cols_size=12,
        title='Usuarios únicos mensuales',
        tabs_index=("MAU_qt", "año a año")
    )
    order += 1

    s.client.plt.update_tabs_group_metadata(
        menu_path=menu_path,
        group_name='MAU',
        order=order,
        sticky=False,
        just_labels=False,
        rows_size=0,
    )
    order += 1

    s.client.plt.doughnut(
        data=reporter.unique_mau_quantity_by_gender_last_month(),
        menu_path=menu_path,
        order=order,
        tabs_index=("MAU", "Revisar mes"),
        cols_size=6,
        rows_size=2
    )
    order += 1

    s.client.plt.rose(
        data=reporter.unique_mau_quantity_by_age_last_month(),
        menu_path=menu_path,
        order=order,
        tabs_index=("MAU", "Revisar mes"),
        cols_size=6,
        rows_size=2
)
    order += 1

    data = reporter.unique_mau_by_activation_code_last_month()
    s.client.plt.bar(
        data=data,
        menu_path=menu_path,
        order=order,
        tabs_index=("MAU", "Revisar mes"),
        cols_size=6,
        rows_size=2,
        x='fecha_alta',
        y=data.columns.drop(['fecha_alta']).tolist(),
    )
    order += 1
    data = reporter.unique_mau_by_cohorte_last_month()
    s.client.plt.bar(
        data=data,
        menu_path=menu_path,
        order=order,
        tabs_index=("MAU", "Revisar mes"),
        cols_size=6,
        rows_size=2,
        x='fecha_alta',
        y=data.columns.drop(['fecha_alta']).tolist(),
    )
    order += 1

    s.client.plt.stacked_barchart(
        data=reporter.unique_mau_quantity_by_gender().tail(12),
        menu_path=menu_path,
        order=order,
        x="fecha_alta",
        x_axis_name='Mes de alta',
        rows_size=3, cols_size=6,
        subtitle='Usuarios únicos por genero',
        tabs_index=("MAU", "Evolución mensual")
    )
    order += 1

    s.client.plt.stacked_horizontal_barchart(
        data=reporter.unique_mau_quantity_by_age().tail(12),
        menu_path=menu_path,
        order=order,
        x="fecha_alta",
        x_axis_name='Mes de alta',
        rows_size=3, cols_size=6,
        tabs_index=("MAU", "Evolución mensual")

    )
    order += 1

    s.client.plt.bar(
        data=reporter.unique_mau_by_activation_code().tail(12),
        menu_path=menu_path,
        order=order,
        x='fecha_alta', y=reporter.df['codigo_activacion'].unique().tolist(),
        rows_size=3, cols_size=6,
        x_axis_name='Mes de alta',
        y_axis_name='Código de activación',
        subtitle='Usuarios únicos por código de referido',
        tabs_index=("MAU", "Evolución mensual"),
    )
    order += 1

    s.client.plt.stacked_area_chart(
        data=reporter.unique_mau_by_cohorte().tail(12),
        menu_path=menu_path,
        order=order,
        cols_size=6, rows_size=3,
        x="fecha_alta",
        x_axis_name='Fecha de alta',
        calculate_percentages=True,
        tabs_index=("MAU", "Evolución mensual"),
    )
    order += 1


if __name__ == '__main__':
    load_dotenv()
    run()
