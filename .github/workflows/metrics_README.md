# Tianji Game Data Monitoring (Template)

# 说明：本文件为数据采集与平衡性分析的CI建议模板。
# 推荐集成到后续自动化流程中，采集如下核心指标：
# - 各卡牌胜率、使用率、平均资源变化、对局时长等
# - 采集脚本建议输出CSV/JSON，供BI分析
#
# 建议：
# 1. 在游戏引擎主循环中埋点，记录每局卡牌使用与结算数据
# 2. 每次CI可自动上传最新数据快照，供平衡性分析
# 3. 可扩展为定期自动生成平衡性报告

# 示例采集脚本入口（需开发者实现）
# python3 tools/collect_game_metrics.py --output metrics/latest_metrics.json

# 示例CI集成片段：
# jobs:
#   metrics:
#     runs-on: ubuntu-latest
#     steps:
#       - uses: actions/checkout@v3
#       - name: Set up Python
#         uses: actions/setup-python@v4
#         with:
#           python-version: '3.10'
#       - name: Run metrics collector
#         run: |
#           python3 tools/collect_game_metrics.py --output metrics/latest_metrics.json
#       - name: Upload metrics artifact
#         uses: actions/upload-artifact@v3
#         with:
#           name: game-metrics
#           path: metrics/latest_metrics.json
