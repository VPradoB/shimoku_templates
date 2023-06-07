from os import getenv

import shimoku_api_python as shimoku


class ShimokuClient:
    def __init__(self):
        access_token = getenv('SHIMOKU_TOKEN')  # env var with your token
        universe_id: str = getenv('UNIVERSE_ID')  # your universe UUID
        business_id: str = getenv('BUSINESS_ID')

        try:
            self.client = shimoku.Client(
                access_token=access_token,
                universe_id=universe_id,
                business_id=business_id,
                verbosity='DEBUG'
            )
        except Exception:
            print('Error al conectar con Shimoku')
            raise Exception('Error al conectar con Shimoku')

    def delete_app(self, app_name: str):
        app_id = self.client.app.get_app_by_name(business_id=self.client.app.business_id, name=app_name)["id"]
        if app_id:
            self.client.app.delete_app(business_id=self.client.app.business_id, app_id=app_id)

    def delete_dashboard(self, dashboard_name):
        self.client.dashboard.delete_dashboard(dashboard_name)

    def create_dashboard(self, dashboard_name):
        self.client.plt.set_dashboard(dashboard_name)
