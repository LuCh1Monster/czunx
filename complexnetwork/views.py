from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from apps.chnx_tools import checkIfExists, plot_chnx, plot_chnx_sample, jsnx


def index(request):
    return render(request, 'dashboard/homepage.html')

def chineseNetwork(request):
    context = {}
    template = loader.get_template('complexnetwork/nx_pyecharts.html')

    if request.method == "POST":
        chinese_character1 = request.POST.get("chineseCharacter1", None)
        chinese_character2 = request.POST.get("chineseCharacter2", None)
        display_sample_network = request.POST.get("displaySampleNetwork", None)

        context['chineseCharacter1'] = chinese_character1
        context['chineseCharacter2'] = chinese_character2
        context['displaySampleNetwork'] = display_sample_network

        if display_sample_network is not None:
            context['displaySampleNetwork'] = "checked"
            context_echarts = plot_chnx_sample()
            context.update(context_echarts)
            context['warMsg'] = "这是样例数据网络图"
            return HttpResponse(template.render(context, request))
        else:
            context['displaySampleNetwork'] = ""


        if chinese_character1 == '' and chinese_character2 == '':
            errMsg = "至少输入第一个汉字后，点击提交!"
            context["errMsg"] = errMsg
        elif chinese_character1 == '' and chinese_character2 != '':
            errMsg = "请先输入第一个汉字后，再输入二个汉字，点击提交!"
            context["errMsg"] = errMsg
        else:
            check_status = checkIfExists(chinese_character1, chinese_character2)
            if check_status == 1:
                warMsg = "输入的汉字2 为空"
                context["warMsg"] = warMsg
                context_echarts = plot_chnx(chinese_character1, chinese_character2, check_code=check_status)
                context.update(context_echarts)
            elif check_status == 2:
                errMsg = "汉字1 不存在数据库中，请重新输入"
                context["errMsg"] = errMsg
            elif check_status == 3:
                errMsg = "汉字1, 汉字2 均不存在数据库中，请重新输入"
                context["errMsg"] = errMsg
            elif check_status == 4:
                context_echarts = plot_chnx(chinese_character1, chinese_character2, check_code=check_status)
                context.update(context_echarts)
            elif check_status == 5:
                warMsg = "输入的汉字2 不在数据库中"
                context["warMsg"] = warMsg
                context_echarts = plot_chnx(chinese_character1, chinese_character2, check_code=check_status)
                context.update(context_echarts)
            elif check_status == 6:
                warMsg = "输入的汉字1 不在数据库中"
                context["warMsg"] = warMsg
                context_echarts = plot_chnx(chinese_character1, chinese_character2, check_code=check_status)
                context.update(context_echarts)
    return HttpResponse(template.render(context, request))

def chineseNetwork2(request):
    context = {}
    template = loader.get_template('complexnetwork/jsnx.html')

    if request.method == "POST":
        chinese_character1 = request.POST.get("chineseCharacter1", None)
        chinese_character2 = request.POST.get("chineseCharacter2", None)
        display_sample_network = request.POST.get("displaySampleNetwork", None)

        context['chineseCharacter1'] = chinese_character1
        context['chineseCharacter2'] = chinese_character2
        context['displaySampleNetwork'] = display_sample_network
        context_jsnx = jsnx(chinese_character1, chinese_character2)
        context.update(context_jsnx)

    return HttpResponse(template.render(context, request))