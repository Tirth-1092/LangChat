

# import json
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from deep_translator import (
#     GoogleTranslator,
#     MyMemoryTranslator,
#     PonsTranslator,
#     LingueeTranslator,
# )
# from deep_translator.exceptions import TranslationNotFound
# from django.utils import timezone

# class ChatConsumer(AsyncWebsocketConsumer):
#     def check_origin(self, origin: str) -> bool:
#         # Allow all origins so the WebSocket stays open
#         return True

#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         print("🐍 [receive] got:", text_data)
#         data     = json.loads(text_data)
#         original = data.get('message', '')

#         # Map human room names → ISO codes for translators
#         iso_map = {
#             'English': 'en',
#             'French':  'fr',
#             'Spanish': 'es',
#             'German':  'de',
#             'Chinese': 'zh-CN',
#             'Hindi':   'hi',
#         }
#         target = iso_map.get(self.room_name, 'en')

#         translated = original  # default fallback

#         # 1) Try GoogleTranslator
#         try:
#             translated = await sync_to_async(
#                 GoogleTranslator(source='auto', target=target).translate
#             )(original)
#             print("🐍 [receive] GoogleTranslator:", translated)
#         except Exception as e:
#             print(f"⚠️ GoogleTranslator failed: {e}, trying MyMemory")

#             # 2) Fallback to MyMemoryTranslator :contentReference[oaicite:7]{index=7}
#             try:
#                 translated = await sync_to_async(
#                     MyMemoryTranslator(source='auto', target=target).translate
#                 )(original)
#                 print("🐍 [receive] MyMemoryTranslator:", translated)
#             except Exception as e2:
#                 print(f"⚠️ MyMemoryTranslator failed: {e2}, trying PONS")

#                 # 3) Fallback to PONS Translator :contentReference[oaicite:8]{index=8}
#                 try:
#                     translated = await sync_to_async(
#                         PonsTranslator(source='auto', target=target).translate
#                     )(original)
#                     print("🐍 [receive] PonsTranslator:", translated)
#                 except Exception as e3:
#                     print(f"⚠️ PonsTranslator failed: {e3}, trying Linguee")

#                     # 4) Fallback to LingueeTranslator :contentReference[oaicite:9]{index=9}
#                     try:
#                         translated = await sync_to_async(
#                             LingueeTranslator(source='auto', target=target).translate
#                         )(original)
#                         print("🐍 [receive] LingueeTranslator:", translated)
#                     except Exception as e4:
#                         print(f"❌ LingueeTranslator failed: {e4} — using original")

#         # Broadcast the final translation (or original fallback)
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type'       : 'chat.message',
#                 'username'   : (
#                     self.scope['user'].username
#                     if self.scope['user'].is_authenticated
#                     else 'Anonymous'
#                 ),
#                 'translation': translated,
#                 'timestamp'  : timezone.now().strftime('%H:%M'),
#             }
#         )

#     async def chat_message(self, event):
#         print("🐍 [chat_message] event:", event)
#         await self.send(text_data=json.dumps({
#             'username'   : event['username'],
#             'translation': event['translation'],
#             'timestamp'  : event['timestamp'],
#         }))


# import json
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from deep_translator import (
#     GoogleTranslator,
#     MyMemoryTranslator,
#     PonsTranslator,
#     LingueeTranslator,
# )
# from deep_translator.exceptions import TranslationNotFound
# from django.utils import timezone

# class ChatConsumer(AsyncWebsocketConsumer):
#     def check_origin(self, origin: str) -> bool:
#         return True

#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         print("🐍 [receive] got:", text_data)
#         data     = json.loads(text_data)
#         original = data.get('message', '')

#         # Map room names to ISO codes
#         iso_map = {
#             'English': 'en',
#             'French':  'fr',
#             'Spanish': 'es',
#             'German':  'de',
#             'Chinese': 'zh-CN',
#             'Hindi':   'hi',
#         }
#         target_lang = iso_map.get(self.room_name, 'en')

#         # Define safe translate function
#         async def safe_translate(text, target):
#             try:
#                 return await sync_to_async(GoogleTranslator(source='auto', target=target).translate)(text)
#             except Exception as e:
#                 print(f"⚠️ Google failed: {e}")
#                 try:
#                     return await sync_to_async(MyMemoryTranslator(source='auto', target=target).translate)(text)
#                 except Exception as e2:
#                     print(f"⚠️ MyMemory failed: {e2}")
#                     try:
#                         return await sync_to_async(PonsTranslator(source='auto', target=target).translate)(text)
#                     except Exception as e3:
#                         print(f"⚠️ PONS failed: {e3}")
#                         try:
#                             return await sync_to_async(LingueeTranslator(source='auto', target=target).translate)(text)
#                         except Exception as e4:
#                             print(f"❌ Linguee failed: {e4}")
#                             return text  # fallback

#         # Step 1: Always translate to English
#         english_text = await safe_translate(original, 'en')

#         # Step 2: If room is not English, translate to target
#         if target_lang != 'en':
#             translated = await safe_translate(english_text, target_lang)
#         else:
#             translated = english_text

#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type'       : 'chat.message',
#                 'username'   : (
#                     self.scope['user'].username
#                     if self.scope['user'].is_authenticated
#                     else 'Anonymous'
#                 ),
#                 'translation': translated,
#                 'timestamp'  : timezone.now().strftime('%H:%M'),
#             }
#         )

#     async def chat_message(self, event):
#         print("🐍 [chat_message] event:", event)
#         await self.send(text_data=json.dumps({
#             'username'   : event['username'],
#             'translation': event['translation'],
#             'timestamp'  : event['timestamp'],
#         }))



# import json
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from deep_translator import (
#     GoogleTranslator,
#     MyMemoryTranslator,
#     PonsTranslator,
#     LingueeTranslator,
# )
# from langdetect import detect
# from django.utils import timezone

# class ChatConsumer(AsyncWebsocketConsumer):
#     def check_origin(self, origin: str) -> bool:
#         # Allow all origins so the WebSocket stays open
#         return True

#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data     = json.loads(text_data)
#         original = data.get('message', '')

#         # 1) Detect the source language
#         try:
#             source_lang = detect(original)
#         except Exception:
#             source_lang = 'en'  # fallback if detection fails :contentReference[oaicite:2]{index=2}

#         # 2) Map room names → ISO codes
#         iso_map = {
#             'English': 'en',
#             'French':  'fr',
#             'Spanish': 'es',
#             'German':  'de',
#             'Chinese': 'zh-CN',
#             'Hindi':   'hi',
#         }
#         room_lang = iso_map.get(self.room_name, 'en')

#         # 3) Decide whether—and where—to translate
#         if source_lang == 'en' and room_lang != 'en':
#             target = room_lang             # English → Room
#         elif source_lang == room_lang and room_lang != 'en':
#             target = 'en'                  # Room → English
#         elif source_lang not in {'en', room_lang}:
#             target = room_lang             # Other → Room
#         else:
#             target = None                  # No translation

#         translated = original
#         if target:
#             # Try GoogleTranslator first
#             try:
#                 translated = await sync_to_async(
#                     GoogleTranslator(source='auto', target=target).translate
#                 )(original)                # auto-detects source internally :contentReference[oaicite:3]{index=3}
#             except Exception:
#                 # Fallback chain
#                 for Translator in (MyMemoryTranslator, PonsTranslator, LingueeTranslator):
#                     try:
#                         translated = await sync_to_async(
#                             Translator(source='auto', target=target).translate
#                         )(original)
#                         break
#                     except Exception:
#                         continue
#                 # if all fail, `translated` stays as `original`

#         # 4) Broadcast result
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type'       : 'chat.message',
#                 'username'   : (
#                     self.scope['user'].username
#                     if self.scope['user'].is_authenticated
#                     else 'Anonymous'
#                 ),
#                 'translation': translated,
#                 'timestamp'  : timezone.now().strftime('%H:%M'),
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'username'   : event['username'],
#             'translation': event['translation'],
#             'timestamp'  : event['timestamp'],
#         }))

#-------------------------------------------------------------------------------------------------------------------------------------------------------


# import json
# import io
# import base64
# from asgiref.sync import sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from deep_translator import (
#     GoogleTranslator,
#     MyMemoryTranslator,
#     PonsTranslator,
#     LingueeTranslator,
# )
# from langdetect import detect
# from gtts import gTTS
# from django.utils import timezone

# class ChatConsumer(AsyncWebsocketConsumer):
#     def check_origin(self, origin: str) -> bool:
#         return True

#     async def connect(self):
#         self.room_name  = self.scope['url_route']['kwargs']['room_name']
#         self.group_name = f'chat_{self.room_name}'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data     = json.loads(text_data)
#         original = data.get('message', '')

#         # 1) detect source language
#         try:
#             source_lang = detect(original)
#         except Exception:
#             source_lang = 'en'

#         # 2) map rooms → ISO codes
#         iso_map = {
#             'English': 'en', 'French': 'fr', 'Spanish': 'es',
#             'German':  'de', 'Chinese': 'zh-CN', 'Hindi': 'hi',
#         }
#         room_lang = iso_map.get(self.room_name, 'en')

#         # 3) decide translation target
#         if source_lang == 'en' and room_lang != 'en':
#             target = room_lang
#         elif source_lang == room_lang and room_lang != 'en':
#             target = 'en'
#         elif source_lang not in {'en', room_lang}:
#             target = room_lang
#         else:
#             target = None

#         # 4) perform translation cascade if needed
#         translated = original
#         if target:
#             try:
#                 translated = await sync_to_async(
#                     GoogleTranslator(source='auto', target=target).translate
#                 )(original)
#             except Exception:
#                 for T in (MyMemoryTranslator, PonsTranslator, LingueeTranslator):
#                     try:
#                         translated = await sync_to_async(
#                             T(source='auto', target=target).translate
#                         )(original)
#                         break
#                     except Exception:
#                         continue

#         # 5) generate TTS audio for both texts
#         def make_base64_audio(text, lang_code):
#             # in-memory MP3 :contentReference[oaicite:3]{index=3}
#             buff = io.BytesIO()
#             gTTS(text=text, lang=lang_code).write_to_fp(buff)  # MP3 bytes :contentReference[oaicite:4]{index=4}
#             buff.seek(0)
#             b64 = base64.b64encode(buff.read()).decode('ascii')  # Base64 :contentReference[oaicite:5]{index=5}
#             return f"data:audio/mp3;base64,{b64}"

#         audio_orig = make_base64_audio(original, source_lang)
#         audio_trans = make_base64_audio(translated, target or source_lang)

#         # 6) broadcast both text + audio URIs
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type'          : 'chat.message',
#                 'username'      : (
#                     self.scope['user'].username
#                     if self.scope['user'].is_authenticated else 'Anonymous'
#                 ),
#                 'original'      : original,
#                 'translation'   : translated,
#                 'audio_orig'    : audio_orig,
#                 'audio_trans'   : audio_trans,
#                 'timestamp'     : timezone.now().strftime('%H:%M'),
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'username'      : event['username'],
#             'original'      : event['original'],
#             'translation'   : event['translation'],
#             'audio_orig'    : event['audio_orig'],
#             'audio_trans'   : event['audio_trans'],
#             'timestamp'     : event['timestamp'],
#         }))


import json
import io
import base64
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from deep_translator import (
    GoogleTranslator,
    MyMemoryTranslator,
    PonsTranslator,
    LingueeTranslator,
)
from langdetect import detect
from gtts import gTTS
from django.utils import timezone
from api.models import ChatRoom, ChatMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    def check_origin(self, origin: str) -> bool:
        return True

    async def connect(self):
        self.room_name  = self.scope['url_route']['kwargs']['room_name']
        self.group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data     = json.loads(text_data)
        original = data.get('message', '')

        # 1) detect source language
        try:
            source_lang = detect(original)
        except Exception:
            source_lang = 'en'

        # 2) map rooms → ISO codes
        iso_map = {
            'English': 'en', 'French': 'fr', 'Spanish': 'es',
            'German':  'de', 'Chinese': 'zh-CN', 'Hindi': 'hi',
        }
        room_lang = iso_map.get(self.room_name, 'en')

        # 3) decide translation target
        if source_lang == 'en' and room_lang != 'en':
            target = room_lang
        elif source_lang == room_lang and room_lang != 'en':
            target = 'en'
        elif source_lang not in {'en', room_lang}:
            target = room_lang
        else:
            target = None

        # 4) perform translation cascade if needed
        translated = original
        if target:
            try:
                translated = await sync_to_async(
                    GoogleTranslator(source='auto', target=target).translate
                )(original)
            except Exception:
                for T in (MyMemoryTranslator, PonsTranslator, LingueeTranslator):
                    try:
                        translated = await sync_to_async(
                            T(source='auto', target=target).translate
                        )(original)
                        break
                    except Exception:
                        continue

        # 5) generate TTS audio for both texts
        def make_base64_audio(text, lang_code):
            buff = io.BytesIO()
            gTTS(text=text, lang=lang_code).write_to_fp(buff)
            buff.seek(0)
            b64 = base64.b64encode(buff.read()).decode('ascii')
            return f"data:audio/mp3;base64,{b64}"

        audio_orig = make_base64_audio(original, source_lang)
        audio_trans = make_base64_audio(translated, target or source_lang)

        # 6) Save the message to the database
        room_obj = await sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        user_obj = self.scope['user'] if self.scope['user'].is_authenticated else None

        if user_obj:
            await sync_to_async(ChatMessage.objects.create)(
                room=room_obj,
                user=user_obj,
                content=original,
                translation=translated
            )
        else:
            anon_user, _ = await sync_to_async(User.objects.get_or_create)(username="Anonymous")
            await sync_to_async(ChatMessage.objects.create)(
                room=room_obj,
                user=anon_user,
                content=original,
                translation=translated
            )

        # 7) Broadcast both text + audio
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type'        : 'chat.message',
                'username'    : user_obj.username if user_obj else "Anonymous",
                'original'    : original,
                'translation' : translated,
                'audio_orig'  : audio_orig,
                'audio_trans' : audio_trans,
                'timestamp'   : timezone.now().strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username'    : event['username'],
            'original'    : event['original'],
            'translation' : event['translation'],
            'audio_orig'  : event['audio_orig'],
            'audio_trans' : event['audio_trans'],
            'timestamp'   : event['timestamp'],
        }))
