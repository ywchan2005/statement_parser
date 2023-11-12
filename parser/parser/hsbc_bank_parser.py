from parser.abstract_parser import AbstractParser


class HsbcBankParser(AbstractParser):
  header_text = 'BALANCE BROUGHT FORWARD'
  footer_text = 'BALANCE CARRIED FORWARD'
  table_header_text = 'Paid out'

  def extract_pageids(self):
    pages = self.pdf.pq(f'LTPage:contains("{HsbcBankParser.footer_text}")')
    pageids = [page.layout.pageid for page in pages]
    return pageids

  def extract_header(self, pageid):
    header = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextBoxHorizontal:contains("{HsbcBankParser.header_text}")')
    if len(header) == 0:
      header = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextBoxHorizontal:contains("{HsbcBankParser.table_header_text}")')
    return header

  def extract_footer(self, pageid):
    footer = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextBoxHorizontal:contains("{HsbcBankParser.footer_text}")')
    return footer

  def extract_amounts(self, pageid, top, bottom):
    paid_outs = self.extract_lines(pageid, (354, bottom, 391, top))
    paid_ins = self.extract_lines(pageid, (437, bottom, 473, top))
    amounts = sorted([*paid_outs, *paid_ins], key=lambda x: x.layout.y0, reverse=True)
    return amounts

  def extract_items(self, pageid, top, bottom):
    items = [self.extract_cell(pageid, (left, bottom, right, top)) for left, right in [
      [52, 88], # payment_date
      # [112, 126], # payment_type
      # [139, 265], # remark
      [112, 265], # remark
    ]]
    return items

  def exclude(self, df):
    return df[
      df.remark.str.startswith(('VIS', ')))', 'DR', 'DD', 'ATM', 'BP')) \
        & (~df.remark.str.contains('HSBC CARD PYMT')) \
        & (~df.remark.str.contains('LLOYDS'))
    ].copy()
