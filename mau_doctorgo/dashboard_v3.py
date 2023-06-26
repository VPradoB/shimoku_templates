import os

from dotenv import load_dotenv

from client import ShimokuClient


def run():
    s = ShimokuClient()
    s.create_dashboard(os.getenv('DASHBOARD_NAME'))
    menu_path = 'mau_v3'
    order = 0

    s.client.plt.html(
        menu_path=menu_path, order=order,
        rows_size=2, cols_size=8,
        html=s.client.html_components.box_with_button(
            title='Dashboard que no sabria como hacer jamas en la vida',
            line='Sub texto que no tenía idea como usar',
            background="https://static.vecteezy.com/system/resources/previews/000/381/988/original/vector-abstract-colorful-dotted-banner-background.jpg",
            href='https://google.com',
            button_text='Visit Google',
        ),
    )
    return s


if __name__ == '__main__':
    load_dotenv('.env.mau')
    dashboard = run()

    dashboard.client.activate_async_execution()
    dashboard.client.run()
