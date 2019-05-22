<template lang="pug">
v-app
  v-navigation-drawer(app, permanent, router)
    v-toolbar
      v-toolbar-title
        nuxt-link.no-underscore(to="/") {{ title }}
    v-divider
    v-list(pt-0)
      v-list-tile(nuxt, to="/visualization")
        v-list-tile-action
          v-icon mdi-chart-bell-curve
        v-list-tile-content
          v-list-tile-title Visualization
      v-list-group(prepend-icon="mdi-thumb-up", v-model="recommendationActive", no-action, active-class="")
        template(slot="activator")
          v-list-tile
            v-list-tile-title Recommendation
        v-list-tile(nuxt, to="/recommendation")
          v-list-tile-content
            v-list-tile-title Simple Filtering
        v-list-tile(nuxt, to="/recommendation2")
          v-list-tile-content
            v-list-tile-title Collaborative Filtering
      v-list-tile(nuxt, to="rate")
        v-list-tile-action
          v-icon mdi-star
        v-list-tile-content
          v-list-tile-title Rate Forecast
  v-content
    v-container(fluid, fill-height)
      nuxt
  v-btn(v-if="$route.name !== 'index'", dark, fab, fixed, bottom, right, @click="showInfo = true")
    v-icon mdi-information-outline
  v-dialog(v-model="showInfo", maxWidth="60%")
    v-card
      v-card-title.headline {{ $route.name }}
      v-card-text(v-html="info[$route.name]")
</template>

<script>
export default {
  data() {
    return {
      title: '',
      showInfo: false,
      recommendationActive: false,
      info: {
        visualization: '<p>综合考量目前流行的若干图标库后，我组最终选择<a href="https://echarts.baidu.com/">Echarts</a>来绘制所有图表。原因如下：</p><ul><li>简单易用：只需要提供key-value对即可绘制图表，且对大量数据有良好的支持</li><li>美观大方：Echarts设计时就重视用户体验，而其配色、交互等已经有完善的一套系统</li><li>扩展性强：图例、工具框等均可自由定制，易于适配各种raw data</li><li>生态良好：Echarts受到一众前端程序员的好评，在Github上维护频繁，且有适配Vue.js的组件，可和其他原生搭配使用的词云图模式等</li></ul>',
        recommendation: '<p>对于电影推荐功能的实现，我组的基本思路是构建一个推荐函数，基于用户的自由输入给出能让用户满意度最高的前10部电影。用于评价这一指标的关键因素便是输入要求与电影属性的相似和匹配程度。基于上述考虑，这一部分主要做的是对于输入和信息的匹配。</p><p>对于电影的演职员、类型以及制片公司，它们都是特定的离散型的一类特征，且在kaggle提供的数据库中已经将上述特征分别分配了ID，因此只需将用户输入的信息转化为ID，直接进行匹配就可以了，匹配程度越高的电影，其推荐指数也越高，</p><p>电影推荐部分中最不可缺少的，最重要的也是最难处理的部分便是关键词（keywords）筛选。由于自然语言系统的复杂性，数据库给出的keywords列表里面的关键词与用户输入的关键词可能互为同义词或近义词，但词形不一样因而导致无法匹配。这里就要使用自然语言处理，参照kaggle数据库中popularity最高的Film Recommendation Kernel，我们使用了NLP中最常用的NLTK Python库，基本思路是扩展用户输入和数据库提供的keywords成为它们同义词根的集合然后再找交集。具体过程是对于kaggle数据库给出的keywords集合，利用NLTK的语料库（Corpus）中的Wordnet，将keywords扩充为其同义词的集合（为了防止过扩充，指定每个词最多扩充为5），考虑到英语单词的多样性，使用其词根则更为合适。因此，再将扩充后的单词集合使用NLTK的stem模块进行词根提取，将提取出的词根记为电影的keywords特征。在进行keywords匹配的时候，对于用户输入的keywords集合用NLTK做与上相同的操作，进而得出扩充后的用户输入keywords的词根集，因而将这两个集合取交集，计算匹配元素个数即可。</p><p>其后是对于综合推荐指数的计算，在这里不能使用简单的匹配个数直接线性求和的方式，因为可能会出现一个特征匹配完全而导致匹配个数很大但是其他特征不匹配的情况。我们使用三重优先级排序的策略，排序顺序为：用户的所有输入是否都得到了一定程度的满足，用户的输入得到一定程度满足的数量，以及最后的匹配个数。这样处理的优点是避免出现上述错误，并使用户要求得到较全面的满足。此外，我们对于这些推荐指标使用电影的综合评分(rate_average)进行加权处理，使得口碑较好的电影可以优先被推荐。为了防止投票样本过少带来的片面性，我们对于综合评分也用评分数量（rate_count）进行评估，对于rate_count过少的电影rate_average做适当减分以避免此种片面性，也减少冷门电影的推荐。而revenue、popularity、rate_count等电影特征在一定程度上都反映的电影的热门程度，是正相关关系，因此调用其中一个特征便可达到目的。最后，使用上述的三重优先级排序将电影列表排序，给出电影列表中前十的电影，即视为推荐给用户的电影。</p>',
        recommendation2: '<p>协同过滤主要是基于“人-物-关联”的数据信息来寻求“人-人”或“物-物”的联系，从而达到优质推荐的目的。在本次项目中，我们处理的数据信息形式为“用户-电影-评分”；面对这样的现有数据，我们可以基于不同对象，有两种选择：</p><ul><li>基于用户：寻求用户之间的关联。以两个用户对各部电影给分的一致与否作为关联的标准，用数据库生成用户形象分类。进行推荐时，系统根据输入的电影生成当前的用户形象，并用户形象类别中进行匹配，最后返回该类普遍给分较高的电影；</li><li>基于电影：寻求电影之间的关联。通过两部电影获得各用户给分的一致与否作为关联标准，用数据库生成“电影-电影”的关联度矩阵。进行推荐时，系统根据输入的多部电影寻求各自关联度最高的多部电影，最后进行综合排序取优。</li></ul><p>然而协同过滤也有它的局限性，不能只靠它来进行推荐：由于用户对电影的评价很大程度与影片质量有关，因此质量相近但风格迥异的电影很有可能也会收获相近的评分，而生成的用户类群也会不甚明晰。因此我们选择先“以物为本”，把第一节“基于内容”评价方式中的数据进行再加工，将“电影-电影”内容属性的相似度提炼出来作为匹配的硬性标准；然后再利用协同过滤这个强有力的人性化推荐手段，让推荐结果不受限于标签和属性的计数，更受到上千万条由真人用户给出的“用户-电影-评分”数据的影响。</p><h4 id="">实施步骤</h4><ol><li>首先，我们利用“用户-电影-评分”数据库计算出了每个用户的平均打分，再将某个用户对某个电影的评分减去该用户的平均给分，将此结果作为该用户对该电影的喜好程度，从而矫正每个用户总体打分偏高或偏低带来的评分误差。</li><li>然后，我们对每两部电影进行分析，将两者共有的打分用户作为参照，把每个用户的给分作为一个维度，在生成的抽象空间中计算两部电影对应的两个抽象向量的夹角，以它的余弦值作为协同过滤生成的该两部电影的关联度。</li><li>最后，为了缩短网页查询时间，在处理“基于内容”评价方式所得数据库时我们只保留了每部电影关联度最高的40部电影，再对这个5000×40的“电影-电影”矩阵中的每个关联度添上我们通过协同过滤所得到的相应“电影-电影”关联度，最终进行关联度的求和、排序，即可得到推荐的电影。</li></ol><p><sim(m_1,m_2)=\\frac{\\sum_u{(R_{um_1}-R_u)(R_{um_2}-R_u)}}{\\sqrt{\\sum_u{(R_{um_1}-R_u)^2}\\cdot \\sum_u{(R_{um_2}-R_u)^2}}}</p><p>其中 $R_{um_i}$ 表示用户 $u$ 对电影 $m_i$ 的评分；$R_u$ 表示用户 $u$ 的平均评分。</p>',
        rate: '暂无。'
      }
    }
  },
  mounted() {
    const pkg = require('../package')
    this.title = pkg.name
  }
}
</script>

<style scoped>
.no-underscore {
  color: black;
  text-decoration: none;
}
</style>
