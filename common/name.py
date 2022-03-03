import random


def random_name():
    # 比较大众化的单姓氏
    surname_single = (
        '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻水云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐费岑薛雷贺倪汤'
        '滕殷罗毕郝邬安常乐于时傅卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计成戴宋茅庞熊纪舒屈项祝董粱杜阮席季麻强贾路娄危江童颜郭'
        '梅盛林刁钟徐邱骆高夏蔡田胡凌霍万柯卢莫房缪干解应宗丁宣邓郁单杭洪包诸左石崔吉龚程邢滑裴陆荣翁荀羊甄家封芮储靳邴松井富乌焦巴弓牧隗山谷车'
        '侯伊宁仇祖武符刘景詹束龙叶幸司韶黎乔苍双闻莘劳逄姬冉宰桂牛寿通边燕冀尚农温庄晏瞿茹习鱼容向古戈终居衡步都耿满弘国文东殴沃曾关红游盖益桓'
        '公晋楚闫'
    )

    # 百家姓中的双姓氏
    surname_double = '万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于' \
                     '闾丘司徒司空亓官司寇仉督端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁段干百里东郭南门呼延羊舌微生梁丘左丘东门西门南宫'
    # 女孩名字
    girl_name = '秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅' \
                '琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希宁欣' \
                '飘育滢馥筠柔竹霭凝晓欢霄枫芸菲寒伊亚宜可姬舒影荔枝思丽'

    # 男孩名字
    boy_name = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清飞彬富顺信子杰涛昌成康星光天达安岩中' \
               '茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭' \
               '鹏泽晨辰士以建家致树炎德行时泰盛雄琛钧冠策腾楠榕风航弘'

    # 名
    mid_name = "中笑贝凯歌易仁器义礼智信友上都卡被好无九加电金马钰玉忠孝"

    # 10%的机遇生成双数姓氏
    if random.choice(range(100)) >= 10:
        surname = surname_single[random.choice(range(len(surname_single)))]
    else:
        i = random.choice(range(len(surname_double)))
        if not i % 2 == 0:
            i += 1
        surname = surname_double[i: i + 2]

    middle_name = ''
    gender = random.choice(range(2))

    # 生成并返回一个名字
    if gender > 0:
        tail_name = girl_name[random.choice(range(len(girl_name)))]
        if random.choice(range(2)) > 0:
            middle_name = mid_name[random.choice(range(len(mid_name)))]
        return surname + middle_name + tail_name
    else:
        tail_name = boy_name[random.choice(range(len(boy_name)))]
        if random.choice(range(2)) > 0:
            middle_name = mid_name[random.choice(range(len(mid_name)))]
        return surname + middle_name + tail_name
