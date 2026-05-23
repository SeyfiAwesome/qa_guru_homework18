import allure
from allure_commons.types import AttachmentType


def take_screenshot(browser_instance):
    png_data = browser_instance.get_screenshot_as_png()
    allure.attach(body=png_data, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def save_browser_logs(browser_instance):
    try:
        logs = browser_instance.get_log('browser')
        log_text = "".join(f'{entry}\n' for entry in logs)
        allure.attach(log_text, 'browser_logs', AttachmentType.TEXT, '.log')
    except:
        allure.attach("No logs available", 'browser_logs', AttachmentType.TEXT, '.log')


def save_page_html(browser_instance):
    html_content = browser_instance.page_source
    allure.attach(html_content, 'page_source', AttachmentType.HTML, '.html')


def add_test_video(browser_instance):
    video_url = f"https://selenoid.autotests.cloud/video/{browser_instance.session_id}.mp4"
    video_tag = f"<html><body><video width='100%' height='100%' controls autoplay><source src='{video_url}' type='video/mp4'></video></body></html>"
    allure.attach(video_tag, f'video_{browser_instance.session_id}', AttachmentType.HTML, '.html')
