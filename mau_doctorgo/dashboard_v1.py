import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from client import ShimokuClient
from mau_doctorgo.mau_reporter import MauReporter


def run():
    df = pd.read_csv('mau_doctorgo/data.csv')
    s = ShimokuClient()
    s.create_dashboard(os.getenv('DASHBOARD_NAME'))
    s.delete_app('Usuarios activos mensuales')
    reporter = MauReporter(df)

    s.client.plt.html(
        html=s.client.html_components.beautiful_indicator(
            title="Usuarios Mensuales Activos UMA",
            href="https://shimoku.io/f4fd08a3-bea2-4b77-90a3-de2b52e8ab74/usuarios-activos-mensuales",
            background_url="https://images.unsplash.com/photo-1628771065518-0d82f1938462",
        ),
        menu_path='Usuarios activos mensuales',
        order=0,
        rows_size=1,
        cols_size=12,
    )
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
        menu_path='Usuarios activos mensuales',
        order=1, rows_size=1, cols_size=12,
        value='value',
        header='title',
        footer='description',
        color='color',
        variant='variant',
    )
    data = reporter.unique_mau_quantity()
    data['fecha_alta'] = data['fecha_alta'].astype(str)
    s.client.plt.line(
        data=data,
        menu_path='Usuarios activos mensuales', order=4,
        x='fecha_alta', y=['cantidad'],
        rows_size=2, cols_size=12,
        title='Usuarios únicos mensuales',
    )

    s.client.plt.stacked_barchart(
        data=reporter.unique_mau_quantity_by_gender(),
        menu_path='Usuarios activos mensuales', order=5,
        x="fecha_alta",
        x_axis_name='Mes de alta',
        rows_size=3, cols_size=12,
        title='Usuarios únicos por genero',
    )

    s.client.plt.stacked_horizontal_barchart(
        data=reporter.unique_mau_quantity_by_age(),
        menu_path='Usuarios activos mensuales', order=6,
        x="fecha_alta",
        x_axis_name='Mes de alta',
        rows_size=3, cols_size=12,
        title='Usuarios únicos por edad',
    )
    s.client.plt.bar(
        data=reporter.unique_mau_by_activation_code(),
        order=7, menu_path='Usuarios activos mensuales',
        x='fecha_alta', y=reporter.df['codigo_activacion'].unique().tolist(),
        rows_size=3, cols_size=12,
        x_axis_name='Mes de alta',
        y_axis_name='Código de activación',
        title='Usuarios únicos por código de referido',
    )

    s.client.plt.stacked_area_chart(
        title='Usuarios únicos por web',
        data=reporter.unique_mau_by_cohorte(),
        menu_path='Usuarios activos mensuales', order=8,
        cols_size=12, rows_size=3,
        x="fecha_alta",
        x_axis_name='Fecha de alta',
        calculate_percentages=True
    )





if __name__ == '__main__':
    load_dotenv()
    run()
