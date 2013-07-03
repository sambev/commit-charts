from jinja2 import Environment, FileSystemLoader
import os

ENV = Environment(
    loader=FileSystemLoader(os.getcwd() + '/templates'),
    block_start_string='[[',
    block_end_string=']]',
    variable_start_string='[-',
    variable_end_string='-]',
    comment_start_string='[#',
    comment_end_string='#]',
)

def render(template, params={}):
    """
    Render the given template with the give params
    """
    template = ENV.get_template(template)
    return template.render(params)
