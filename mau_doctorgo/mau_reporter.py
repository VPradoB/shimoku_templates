import unicodedata

import numpy as np
import pandas as pd


class MauReporter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.sanitize_dataframe()

    def sanitize_dataframe(self):
        """Sanitize the dataframe."""
        self.df['codigo_activacion'] = self.df['codigo_activacion'].replace(np.nan, 'Sin Código').astype(str)
        self.df['codigo_activacion'] = self.df['codigo_activacion'].apply(
            lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8').capitalize().strip()
        )
        #
        # self.df['cohorte'] = self.df['cohorte'].apply(
        #     lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8').capitalize().strip()
        # )
        #
        # self.df['genero'] = self.df['genero'].apply(
        #     lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode('utf-8').capitalize().strip()
        # )

        self.df['fecha_alta'] = pd.to_datetime(self.df['fecha_alta'], format='%d/%m/%Y')
        self.df['edad'] = pd.to_numeric(self.df['edad'], errors='raise')

    def unique_mau_quantity_current_month(self):
        """Unique MAU quantity."""
        hoy = pd.to_datetime('today')
        primer_dia_mes_actual = pd.to_datetime('today').replace(day=1)
        return len(self.df[(self.df['fecha_alta'] >= primer_dia_mes_actual)
                           & (self.df['fecha_alta'] <= hoy)])

    def unique_mau_quantity_previous_month(self):
        """Unique MAU quantity."""
        primer_dia_mes_actual = pd.to_datetime('today').replace(day=1)
        primer_dia_mes_anterior = primer_dia_mes_actual - pd.DateOffset(months=1)
        return len(self.df[(self.df['fecha_alta'] >= primer_dia_mes_anterior)
                           & (self.df['fecha_alta'] < primer_dia_mes_actual)])

    def unique_mau_quantity(self):
        unique_users_monthly = self.df.groupby(self.df['fecha_alta'].dt.to_period('M')).size() \
            .reset_index(name='cantidad')
        return unique_users_monthly

    def unique_mau_quantity_yearly(self):
        unique_users_monthly = self.unique_mau_quantity()
        unique_users_monthly['Mes'] = unique_users_monthly['fecha_alta'].dt.strftime('%m')
        unique_users_monthly['Año'] = unique_users_monthly['fecha_alta'].dt.strftime('%Y')
        return unique_users_monthly.pivot(index='Mes', columns='Año', values='cantidad').fillna(0).reset_index()

    def unique_mau_quantity_by_gender(self):
        unique_users_monthly = self.df.groupby([self.df['fecha_alta'].dt.strftime('%Y-%m'), 'genero'])['id'].nunique() \
            .unstack('genero').reset_index().rename_axis(None, axis=1)
        unique_users_monthly['fecha_alta'] = unique_users_monthly['fecha_alta'].astype(str)
        return unique_users_monthly.fillna(0)

    def unique_mau_quantity_by_gender_last_month(self):
        unique_users_monthly = self.unique_mau_quantity_by_gender().tail(1).drop(columns=['fecha_alta'], axis=1)
        return unique_users_monthly.melt(var_name='name', value_name='value').query('value > 0')

    def unique_mau_quantity_by_age(self):
        age_intervals = [
            (21, 30),
            (31, 40),
            (41, 50),
            (51, 60),
            (61, 70),
            (71, 79)
        ]
        self.df['edad_intervalo'] = pd.cut(self.df['edad'],
                                           bins=[interval[0] for interval in age_intervals] + [
                                               age_intervals[-1][1] + 1],
                                           labels=[f"{interval[0]}-{interval[1]}" for interval in age_intervals])

        unique_users_by_age = self.df.groupby([self.df['fecha_alta'].dt.strftime('%Y-%m'), 'edad_intervalo'])[
            'id'].nunique().unstack('edad_intervalo').reset_index().rename_axis(None, axis=1)
        unique_users_by_age['fecha_alta'] = unique_users_by_age['fecha_alta'].astype(str)
        return unique_users_by_age

    def unique_mau_quantity_by_age_last_month(self):
        unique_users_monthly = self.unique_mau_quantity_by_age().tail(1).drop(columns=['fecha_alta'], axis=1)
        return unique_users_monthly.melt(var_name='name', value_name='value').query('value > 0')

    def unique_au_quantity(self):
        return self.df.shape[0]

    def unique_mau_by_activation_code(self):
        unique_users_monthly = self.df.groupby([self.df['fecha_alta'].dt.strftime('%Y-%m'), 'codigo_activacion'])['id'].nunique() \
            .unstack('codigo_activacion').reset_index().rename_axis(None, axis=1)
        unique_users_monthly['fecha_alta'] = unique_users_monthly['fecha_alta'].astype(str)
        return unique_users_monthly.fillna(0)

    def unique_mau_by_activation_code_last_month(self):
        unique_users_monthly = self.unique_mau_by_activation_code().tail(1)
        return unique_users_monthly

    def unique_mau_by_cohorte(self):
        unique_users_monthly = self.df.groupby([self.df['fecha_alta'].dt.strftime('%Y-%m'), 'cohorte'])['id'].nunique()\
            .unstack('cohorte').reset_index().rename_axis(None, axis=1)
        unique_users_monthly['fecha_alta'] = unique_users_monthly['fecha_alta'].astype(str)
        return unique_users_monthly.fillna(0)

    def unique_mau_by_cohorte_last_month(self):
        unique_users_monthly = self.unique_mau_by_cohorte().tail(1)
        return unique_users_monthly

if __name__ == '__main__':
    df = pd.read_csv('mau_doctorgo/data.csv')
    reporter = MauReporter(df)
    print(reporter.unique_mau_quantity_by_gender())