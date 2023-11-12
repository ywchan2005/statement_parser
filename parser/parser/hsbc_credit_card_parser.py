from parser.abstract_parser import AbstractParser


class HsbcCreditCardParser(AbstractParser):
  header_text = 'Your Transaction Details'
  footer_text = 'Summary Of Interest On This Statement'

  def extract_pageids(self):
    start = self.pdf.pq(f'LTPage:contains("{HsbcCreditCardParser.header_text}")')
    assert len(start) == 1
    end = self.pdf.pq(f'LTPage:contains("{HsbcCreditCardParser.footer_text}")')
    assert len(end) == 1
    return range(start[0].layout.pageid, end[0].layout.pageid + 1)

  def extract_header(self, pageid):
    header = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextLineHorizontal:contains("{HsbcCreditCardParser.header_text}")')
    return header

  def extract_footer(self, pageid):
    footer = self.pdf.pq(f'LTPage[pageid="{pageid}"] LTTextLineHorizontal:contains("{HsbcCreditCardParser.footer_text}")')
    return footer

  def extract_amounts(self, pageid, top, bottom):
    amounts = self.extract_lines(pageid, (509, bottom, 564, top))
    amounts = sorted(amounts, key=lambda x: x.layout.y0, reverse=True)
    return amounts

  def extract_items(self, pageid, top, bottom):
    items = [self.extract_cell(pageid, (left, bottom, right, top)) for left, right in [
      [52, 104], # payment_date
      # [117, 169], # transaction_date
      [196, 424], # remark
    ]]
    return items

  def exclude(self, df):
    return df[
      ~df.remark.str.contains('DIRECT DEBIT PAYMENT - THANK YOU')
    ].copy()
