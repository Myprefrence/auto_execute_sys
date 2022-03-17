import random
class Phone(object):
    # 随机生成手机号码

    def phoneRandom(self):
        prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
        return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

    def sesssionRandom(self):
        prelist=["test_","bing_","ai_","niu_","sheng_","yang_","wang_","jun_"]
        return random.choice(prelist)+"".join(random.choice("0,10000000") for i in range(3))

    def textRandom(self):
        prelist=["wo","ai","ni","yi","sheng","yi","niu"]
        return random.choice(prelist)+"".join(random.choice("abcdefgrjhklmnopquvwxyz123456789UV") for i in range(3))




if __name__ == '__main__':
    pg = Phone()
    print(pg.sesssionRandom())