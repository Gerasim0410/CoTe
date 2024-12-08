# channel_views.py
import json
import logging

from django.shortcuts import reverse
from django.templatetags.static import static

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .views import process_test_submission, logger
from .models import TestSession, Questions


class QuizConsumer(AsyncWebsocketConsumer):

    # connection function, assigns groups to specific users
    async def connect(self):
        logger.log(msg='in connect', level=logging.DEBUG)
        if self.scope['user'].is_authenticated:
            logger.log(msg='in connect in if', level=logging.DEBUG)
            self.user_id = self.scope['user'].user_id
            self.is_first_user = self.user_id == 1
            self.group_name = f"quiz_group_{self.is_first_user}"
            await self.accept()
            await self.channel_layer.group_add(
                self.group_name, self.channel_name)
            logger.log(msg='connection accepted',
                       level=logging.DEBUG)
        else:
            await self.close()
            logger.log(msg='connection refused', level=logging.DEBUG)

    # disconnect function, removes users from the group
    async def disconnect(self, close_code):
        logger.log(msg=f'{close_code}', level=logging.DEBUG)
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name)
        logger.log(msg='connection accepted', level=logging.DEBUG)

    # function handling messages TO client
    async def receive(self, text_data):
        data = json.loads(text_data)
        # get test questions
        if data.get('type') == 'test_async':
            await self.test_async(data.get('test'))
        # submit and process data
        elif data.get('type') == 'test_submit_async':
            await self.test_submit_async(text_data)
        # for stroop instruction
        elif data.get('type') == 'instr':
            logger.log(msg=f'{data.get("test")}', level=logging.DEBUG)
            test = data.get('test')[:-1].split('/')[-1]
            if int(test[-1]) < 4:
                await self.channel_layer.group_send(
                    'quiz_group_True',
                    {
                        'type': 'send_stroop_instr',
                        'url': '/instruction/stroop' + str(int(test[-1]) + 1)
                    })
                await self.channel_layer.group_send(
                    'quiz_group_False',
                    {
                        'type': 'send_stroop_instr',
                        'url': '/test/stroop' + test[-1]
                    })
            elif int(test[-1]) == 4:
                await self.channel_layer.group_send(
                    'quiz_group_True',
                    {
                        'type': 'send_stroop_instr',
                        'url': '/instruction/arithm'
                    })
                await self.channel_layer.group_send(
                    'quiz_group_False',
                    {
                        'type': 'send_stroop_instr',
                        'url': '/test/stroop' + test[-1]
                    })

    # stroop instruction handler
    async def send_stroop_instr(self, event):
        await self.send(text_data=json.dumps({
            'url': event['url']
        }))

    # test data handler
    async def send_test_data(self, event):
        await self.send(text_data=json.dumps({
            'select_url': event['select_url'],
            'submit_url': event['submit_url'],
            'test_url': event['test_url'],
            'test': event['test'],
            'group': event['group'],
        }))
        logger.log(msg='connection accepted', level=logging.DEBUG)

    # test display function, contains all required information to render
    # the test template
    async def test_async(self, test):
        logger.log(msg='in test_async', level=logging.DEBUG)
        await self.channel_layer.group_send(
            'quiz_group_False',
            {
                'type': 'send_test_data',
                # url for select
                'select_url': static('js/select.js'),
                # url for submit
                'submit_url': static('js/submit.js'),
                # redirection url for mobile devices after the current test
                # should point to the following test's submission function
                # (test_submit_async)
                'test_url': 'test_submit_async',
                # the following test's name for its future loading
                'test': test,
                'group': 'quiz_group_False',
            })
        logger.log(msg='in test_async before for', level=logging.DEBUG)
        for idx, i in enumerate(Questions.TEST_TYPES):
            if test == i[1] and i != Questions.TEST_TYPES[-1]:
                next_test = Questions.TEST_TYPES[idx + 1][1]
                await self.channel_layer.group_send(
                    'quiz_group_True',
                    {
                        'type': 'send_test_data',
                        # url for select
                        'select_url': static('js/async_select.js'),
                        # url for submit
                        'submit_url': static('js/async_submit.js'),
                        # redirection url for big screen after the current test
                        # should point to the following test's instruction or
                        # to the end of the program
                        'test_url': reverse('instruction',
                                            kwargs={'test': next_test}),
                        'test': test,
                        'group': 'quiz_group_True'
                    })
                logger.log(msg='end test_async instruction True',
                           level=logging.DEBUG)
            elif test == i[1]:
                await self.channel_layer.group_send(
                    'quiz_group_True',
                    {
                        'type': 'send_test_data',
                        # name of async template
                        'template_name': 'async_big_',
                        # redirection url for big screen after the current test
                        # should point to the following test's instruction or
                        # to the end of the program
                        'test_url': reverse('end_test'),
                        'select_url': static('js/async_select.js'),
                        'submit_url': static('js/async_submit.js'),
                        'test': test,
                        'group': 'quiz_group_True'
                    })
                logger.log(msg='end test_async end True',
                           level=logging.DEBUG)

    async def test_submit_async(self, text_data):
        data = json.loads(text_data)
        test = data.get("test", [])
        if self.group_name == 'quiz_group_False':
            test_session = database_sync_to_async(
                TestSession.objects.filter(
                    user_id=self.scope['user'].user_id).last)
            answers_data = data.get("answers", [])

            result = database_sync_to_async(
                process_test_submission)(test_session, answers_data, test)

            logger.log(msg=f'{result}', level=logging.DEBUG)

        for idx, i in enumerate(Questions.TEST_TYPES):
            if test == i[1] and i != Questions.TEST_TYPES[-1]:
                next_test = Questions.TEST_TYPES[idx + 1][1]
                await self.send(text_data=json.dumps(
                    {
                        'message': 'Тест закончен!',
                        'redirect_url': reverse('instruction',
                                                kwargs={'test': next_test})
                    }))
                logger.log(msg='end test_submit_async instruction',
                           level=logging.DEBUG)
            elif test == i[1]:
                await self.send(text_data=json.dumps(
                    {
                        'message': 'Тест закончен!',
                        'redirect_url': reverse('end_test')
                    }))
                logger.log(msg='end test_submit_async end',
                           level=logging.DEBUG)
