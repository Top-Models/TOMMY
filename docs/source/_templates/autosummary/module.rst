{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   {% for class in classes %}
   .. autoclass:: {{ class }}
       :members:
       :undoc-members:
       :show-inheritance:
   {% endfor %}

   {% endif %}
   {% endblock %}

{% block modules %}
{% if modules %}


**Sub-Modules**

.. autosummary::
   :toctree: _autosummary
   :recursive:
    {% for item in modules %}
       {{ item }}
    {%- endfor %}

{% endif %}

{% endblock %}
