import unicodedata

import numpy as np
import pandas as pd


class RecyclerReporter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.sanitize_dataframe()

    def sanitize_dataframe(self):
        """Sanitize the dataframe."""
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], format='%d/%m/%Y')
        self.df['recycled_at'] = pd.to_datetime(self.df['recycled_at'], format='%d/%m/%Y')

    def top_recycled_brands(self):
        """Unique MAU quantity."""
        return self.df.groupby('Brand')['ticketId'].nunique().sort_values(ascending=False).reset_index(name='recycled_qt')

    def recycled_products_by_platform(self):
        """Unique MAU quantity."""
        return self.df.groupby('recycled_platform')['ticketId'].nunique().sort_values(ascending=False).reset_index(name='recycled_qt')

    def recycled_products_by_brand(self):
        """Unique MAU quantity."""
        return self.df.groupby('Brand')['ticketId'].nunique().sort_values(ascending=False).reset_index(name='recycled_qt')

    def recycled_products_by_brand_and_platform_and_month(self):
        """Unique MAU quantity."""
        return self.df.groupby([self.df['recycled_at'].dt.strftime('%Y-%m'), 'Brand', 'recycled_platform'])['ticketId'].nunique().reset_index(name='recycled_qt')

    def recycled_products_by_gender(self):
        """Unique MAU quantity."""
        return self.df.groupby('genero_user')['ticketId'].nunique().sort_values(ascending=False).reset_index(name='recycled_qt')

    def recycled_products_qt(self):
        """Unique MAU quantity."""
        return self.df['recycled_qt'].sum()

    def recycled_products_by_month(self):
        """Unique MAU quantity."""
        return self.df.groupby(self.df['recycled_at'].dt.strftime('%Y-%m'))['recycled_qt'].sum().reset_index(name='recycled_qt')

    def sold_products_qt(self):
        """Unique MAU quantity."""
        return self.df['cantidad'].sum()

    def sold_products_by_month(self):
        """Unique MAU quantity."""
        return self.df.groupby(self.df['created_at'].dt.strftime('%Y-%m'))['cantidad'].sum().reset_index(name='sold_qt')

    def sales_with_problems(self):
        """Unique MAU quantity."""
        return self.df[self.df['anomalía']]

    def recycled_products_percentage(self):
        """Unique MAU quantity."""
        return round(self.recycled_products_qt() / self.sold_products_qt() * 100, 2)

    def recycled_products_percentage_by_month(self):
        """Recycled products percentage by month"""
        return round(self.recycled_products_by_month().tail(1).values[0][1] / self.sold_products_by_month().tail(1).values[0][1] * 100, 2)

    def gender_comparative(self):
        """"Gender comparative."""
        comparativa_generos = self.df.groupby('gender').agg({
            'points_used': 'sum',
            'cantidad': 'sum',
            'recycled_qt': 'sum',
            'anomalía': lambda x: (x).sum(),
        }).reset_index()

        comparativa_generos['porcentaje_reciclado'] = comparativa_generos.apply(lambda row: round(row['recycled_qt'] / row['cantidad'] * 100, 2), axis=1)
        comparativa_generos['porcentaje_anomalia'] = comparativa_generos.apply(lambda row: round(row['anomalía'] / row['cantidad'] * 100, 2), axis=1)
        comparativa_generos['promedio_puntos_usados'] = comparativa_generos.apply(lambda row: round(row['cantidad'] / row['points_used'] * 100, 2), axis=1)

        return comparativa_generos[['gender', 'porcentaje_reciclado', 'porcentaje_anomalia', 'promedio_puntos_usados']]

    def month_comparative(self):
        """Month comparative."""
        resultados_por_mes = self.df.resample('M', on='created_at').agg({
            'cantidad': 'sum',
            'recycled_qt': 'sum',
            'non_recycled_qt': 'sum',
            'anomalía': lambda x: (x).sum()

        }).rename(columns={'cantidad': 'productos_vendidos', 'anomalía': 'anomalías'})
        resultados_por_mes['mes'] = resultados_por_mes.index.strftime('%Y-%m')

        return resultados_por_mes

    def month_sells_comparative_by_brand(self):
        """Month comparative by brand."""
        unique_brands_monthly = self.df.groupby([self.df['created_at'].dt.strftime('%Y-%m'), 'Brand'])['cantidad'].sum() \
            .unstack('Brand').reset_index().rename_axis(None, axis=1)

        unique_brands_monthly['mes'] = unique_brands_monthly['created_at'].astype(str)
        return unique_brands_monthly.fillna(0)[unique_brands_monthly.drop('created_at', axis=1).columns.tolist()]

    def month_sells_comparative_by_platform(self):
        """Month comparative by brand."""
        unique_brands_monthly = self.df.groupby([self.df['created_at'].dt.strftime('%Y-%m'), 'recycled_platform'])['cantidad'].sum() \
            .unstack('recycled_platform').reset_index().rename_axis(None, axis=1)

        unique_brands_monthly['mes'] = unique_brands_monthly['created_at'].astype(str)
        return unique_brands_monthly.fillna(0)[unique_brands_monthly.drop('created_at', axis=1).columns.tolist()]

    def month_recycle_comparative_by_brand(self):
        """Month comparative by brand."""
        unique_brands_monthly = self.df.groupby([self.df['created_at'].dt.strftime('%Y-%m'), 'Brand'])['recycled_qt'].sum() \
            .unstack('Brand').reset_index().rename_axis(None, axis=1)

        unique_brands_monthly['mes'] = unique_brands_monthly['created_at'].astype(str)
        return unique_brands_monthly.fillna(0)[unique_brands_monthly.drop('created_at', axis=1).columns.tolist()]

    def month_recycle_comparative_by_platform(self):
        """Month comparative by brand."""
        unique_brands_monthly = self.df.groupby([self.df['created_at'].dt.strftime('%Y-%m'), 'recycled_platform'])['recycled_qt'].sum() \
            .unstack('recycled_platform').reset_index().rename_axis(None, axis=1)

        unique_brands_monthly['mes'] = unique_brands_monthly['created_at'].astype(str)
        return unique_brands_monthly.fillna(0)[unique_brands_monthly.drop('created_at', axis=1).columns.tolist()]


class TodayReporter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.sanitize_dataframe()

    def sanitize_dataframe(self):
        """Sanitize the dataframe."""
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], format='%d/%m/%Y')
        self.df['householdId'] = self.df['householdId'].fillna(0).astype(int)


if __name__ == '__main__':
    df1 = pd.read_csv('sales.csv')
    df2 = pd.read_csv('users.csv')
    df = pd.merge(df1, df2, on='client_id', how='inner', suffixes=('', '_user'))
    reporter = RecyclerReporter(df)
    primer_dia_mes = pd.Timestamp.now().to_period('M').to_timestamp()
    data = reporter.sales_with_problems()
    print(reporter.month_sells_comparative_by_platform().tail(1).drop('mes', axis=1).melt(var_name='name', value_name='value'))
