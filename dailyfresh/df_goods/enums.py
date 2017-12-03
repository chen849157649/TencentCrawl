"""
Field Types
choices 一个2元元组的元组或者列表,如果执行 choices,
 Django的admin就会使用选择框而不是标准的text框填写这个field
 2元元组的第一个元素是要存入database的数据，
 第二个元素是 admin 的界面显示的数据。
 使用了choices参数的field在其model示例里，
 可以用"get_field的名字_display"方法显示choices的显示字串（就是2元元组的第二个数据）
"""
"""goods_type_choices = ((1, '新鲜水果'),
                  (2, '海鲜水产'),
                  (3, '猪牛羊肉'),
                  (4, '禽类蛋品'),
                  (5, '新鲜蔬菜'),
                  (6, '速冻食品'))
 status_choices = ((0, '下线'), (1, '上线'))"""
# 因为第一参数是要存入database的数据，为了见名知意
# 可考虑有映射作用的字典，然后使用字典生成列表（即列表生成式）
FRUIT=1
SEAFOOD=2
MEAT=3
EGGS=4
VEGETABLES=5
FROZEN=6

GOODS_TYPE = {
    FRUIT:'新鲜水果',
    SEAFOOD:'海鲜水产',
    MEAT:'猪牛羊肉',
    EGGS:'禽类蛋品',
    VEGETABLES:'新鲜蔬菜',
    FROZEN:'速冻食品'
}

OFFLINE=0
ONLINE=1

STATUS_CHOICE = {
    OFFLINE:'下线',
    ONLINE:'上线'
}