from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from .forms import *
from smtplib import SMTP, SMTPAuthenticationError
from email.mime.text import MIMEText

class EPaperView(FormView):
    template_name = "epaper/epaper.html"
    form_class = EPaperForm
    success_url = '/epaper/thanks/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not EPaperEmail.objects.filter(email=self.object.email):
            self.object.save()

            e_mail = self.object.email
            strSmtp = "smtp.gmail.com:587"
            strAccount = "90818126@gcloud.csu.edu.tw"
            strPD = ""
            indexAddr = 'https://example.com'  # 設定你的網站連結
            content = f' <h2>測試寄件成功!!!</h2><p>感謝您瀏覽本網站!!!</p><br>' \
					  f'<p>網站連結:{indexAddr}</p>'
            msg = MIMEText(content, "html")
            msg["Subject"] = "試寄件成功!!!"
            server = SMTP(strSmtp)
            server.ehlo()
            server.starttls()
            try:
                server.login(strAccount, strPD)
                server.sendmail(strAccount, e_mail, msg.as_string())
                mailhint = "郵件已發送！"
            except SMTPAuthenticationError:
                mailhint = "無法登入！"
            except:
                mailhint = "郵件發送產生錯誤！"
            server.quit()

        return super().form_valid(form)
    
class EPaperThanksView(TemplateView):
    template_name = "epaper/thanks.html"