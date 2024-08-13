import ax.processor


SAVER_URL = 'https://saver-api.goscraping.com'

app, processor = ax.processor.AppProcessor(SAVER_URL)


@processor.task()
def demo(self, **kwargs):
    print(f'demo! - {kwargs=}')

    # if i < 10:
    #     self.new_task(i+1, demo=i*12, queue='hello_queue')

    return {'a':42}




if __name__ == "__main__":
    demo.si().apply_async(queue='hello_queue')