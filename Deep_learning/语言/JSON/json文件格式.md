# json 文件格式
JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。JSON采用完全独立于语言的文本格式，这些特性使JSON成为理想的数据交换语言。易于人阅读和编写，同时也易于机器解析和生成。

## JSON 文件结构
1. 名称/值”对的集合（A collection of name/value pairs）
    * 不同的语言中，它被理解为对象（object），记录（record），结构（struct），字典（dictionary），哈希表（hash table），有键列表（keyed list），或者关联数组 （associative array）
2. 值的有序列表（An ordered list of values）
    * 在大部分语言中，它被理解为数组（array）
```json
{
  "squadName": "Super hero squad",
  "homeTown": "Metro City",
  "formed": 2016,
  "secretBase": "Super tower",
  "active": true,
  "members": [
    {
      "name": "Molecule Man",
      "age": 29,
      "secretIdentity": "Dan Jukes",
      "powers": ["Radiation resistance", "Turning tiny", "Radiation blast"]
    },
    {
      "name": "Madame Uppercut",
      "age": 39,
      "secretIdentity": "Jane Wilson",
      "powers": [
        "Million tonne punch",
        "Damage resistance",
        "Superhuman reflexes"
      ]
    },
    {
      "name": "Eternal Flame",
      "age": 1000000,
      "secretIdentity": "Unknown",
      "powers": [
        "Immortality",
        "Heat Immunity",
        "Inferno",
        "Teleportation",
        "Interdimensional travel"
      ]
    }
  ]
}

```
## 示例
### 表示名称 / 值对
最简单的形式，表示 "名称 / 值对"
```json
{ "firstName": "Brett" }
```
多个"名称 / 值对"串在一起时
```json
{ "firstName": "Brett", "lastName":"McLaughlin", "email": "aaaa" }
```
### 表示数组
```json
{ "people": [

{ "firstName": "Brett", "lastName":"McLaughlin", "email": "aaaa" },

{ "firstName": "Jason", "lastName":"Hunter", "email": "bbbb"},

{ "firstName": "Elliotte", "lastName":"Harold", "email": "cccc" }

]}
```
* 只有一个名为 people的变量，值是包含三个条目的数组，每个条目是一个人的记录，其中包含名、姓和电子邮件地址

多个值（每个值包含多个记录）
```json
{ "programmers": [

{ "firstName": "Brett", "lastName":"McLaughlin", "email": "aaaa" },

{ "firstName": "Jason", "lastName":"Hunter", "email": "bbbb" },

{ "firstName": "Elliotte", "lastName":"Harold", "email": "cccc" }

],

"authors": [

{ "firstName": "Isaac", "lastName": "Asimov", "genre": "science fiction" },

{ "firstName": "Tad", "lastName": "Williams", "genre": "fantasy" },

{ "firstName": "Frank", "lastName": "Peretti", "genre": "christian fiction" }

],

"musicians": [

{ "firstName": "Eric", "lastName": "Clapton", "instrument": "guitar" },

{ "firstName": "Sergei", "lastName": "Rachmaninoff", "instrument": "piano" }

] }
```

