# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\ai_eng.py\feathr_project.py\feathr.py\definition.py\materialization_utils_842541f2f9a8.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\ai-eng\feathr_project\feathr\definition\_materialization_utils.py

from feathr.definition.materialization_settings import MaterializationSettings

from jinja2 import Template


def _to_materialization_config(settings: MaterializationSettings):
    # produce materialization config

    tm = Template("""

            operational: {

            name: {{ settings.name }}

            endTime: "{{ settings.backfill_time.end.strftime('%Y-%m-%d %H:%M:%S') }}"

            endTimeFormat: "yyyy-MM-dd HH:mm:ss"

            resolution: {{ settings.resolution }}

            {% if settings.has_hdfs_sink == True %}

            enableIncremental = true

            {% endif %}

            output:[

                    {% for sink in settings.sinks %}

                        {{sink.to_feature_config()}}

                    {% endfor %}

                ]

            }

        features: [{{','.join(settings.feature_names)}}]

    """)

    msg = tm.render(settings=settings)

    return msg
