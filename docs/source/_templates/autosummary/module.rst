{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   {% for class in classes %}
   .. autoclass:: {{ class }}
       :members:
       :undoc-members:
       :inherited-members:

       {% block attributes %}
       {% if attributes %}
       .. rubric:: Attributes

       .. autosummary::
       {% for item in attributes %}
          ~{{ name }}.{{ item }}
       {%- endfor %}
       {% endif %}
       {% endblock %}

       {% block methods %}
       {% if methods %}
       .. rubric:: Methods

       .. autosummary::
       {% for item in all_methods %}
          {%- if not item.startswith('_') %}
          ~{{ name }}.{{ item }}
          {%- endif -%}
       {%- endfor %}
       {% endif %}

       {% endblock %}
   {% endfor %}

   .. autosummary::
      :toctree:
      :template: autosummary/class.rst
       {% for item in classes %}
          {{ item }}
       {%- endfor %}
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
