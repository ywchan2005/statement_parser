from parser.abstract_parser import AbstractParser


class LloydsBankParser(AbstractParser):
  header_text = 'STATEMENT OPENING BALANCE'
  footer_text = 'STATEMENT CLOSING BALANCE'

  def extract_pageids(self):
    pages = self.pdf.pq(f'LTPage:contains("{LloydsBankParser.footer_text}")')
    pageids = [page.layout.pageid for page in pages]
    return pageids

  def extract_header(self, pageid):
    header = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextLineHorizontal:contains("{LloydsBankParser.header_text}")')
    return header

  def extract_footer(self, pageid):
    footer = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextLineHorizontal:contains("{LloydsBankParser.footer_text}")')
    return footer

  def extract_amounts(self, pageid, top, bottom):
    money_outs = self.extract_lines(pageid, (242, bottom, 406, top))
    money_ins = self.extract_lines(pageid, (436, bottom, 477, top))
    amounts = sorted([*money_outs, *money_ins], key=lambda x: x.layout.y0, reverse=True)
    return amounts

  def extract_items(self, pageid, top, bottom):
    items = [self.extract_cell(pageid, (left, bottom, right, top)) for left, right in [
      [53, 122], # payment_date
      # [117, 169], # transaction_date
      # [104, 424], # remark
      [104, 313], # remark
    ]]
    return items

  def exclude(self, df):
    return df[
      ~df.remark.str.startswith('FPI') \
      & ~df.remark.str.contains('CLUB LLOYDS') \
      & ~df.remark.str.contains('INTEREST') \
      & ~df.remark.str.contains('LB RICHMOND')
    ].copy()
