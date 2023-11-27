# vlabeler-vocaloid
a vlabeler of vocaloid db develop with the translate script to transfrom the label to seg file and as file.
这是一个用于进行vocaloid开发的标注器，包含一个脚本用于将标注转换为seg和as文件

# basic
labeler base on vlabeler https://github.com/sdercolin/vlabeler
标注器基于科林的vlabeler运行，转换脚本基于python3，并且使用nuitk进行了编译

# other
标注线的快捷键依次是qwert
请注意标注过程中的区间问题，不要做过长的标注。

![e00bcea1c13688dabfd27290e16a2427](https://github.com/mhbalthasar/vlabeler-vocaloid/assets/98707331/2c1a1f43-33c7-4981-8951-507c4456da63)


# change log
v6:
增加了thirdphontic的支持。由于thirdphontic需要7条线。phoneme2是同音素过渡段，因此在标记过程中thirdphontic被拆成了两个标记组。例如：音素[a b c]，会被拆分为[(a b) c]和[a (b c)]两个标记对象。
标记对象[(a b) c]的start，ph1，ph2 线 和 标记对象 [a (b c)] 的 ph1，ph2，ed，end线 会在transfrom的过程中被分别标记为thirdphontic的start，ph1，ph2.1，ph2.2，ph3，ed，end线。

|三音素标记线|标记名|标记线|
|------|--------------|------|
|start|[(a b) c]|start|
|phoneme1|[(a b) c]|ph1|
|phoneme2.1|[(a b) c]|ph2|
|phoneme2.2|[a (b c)]|ph1|
|phoneme3|[a (b c)]|ph2|
|ed|[a (b c)]|ed|
|end|[a (b c)]|end|
