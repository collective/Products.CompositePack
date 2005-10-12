# Patch CompositePage so that error messages have an appropriate
# class. This lets us suppress the display for anonymous users.
import Products.CompositePage.slot

error_tag = '''<span class="slot_error">%s
(<a href="%s" onmousedown="document.location=this.href">log</a>)</span>'''
Products.CompositePage.slot.error_tag = error_tag
