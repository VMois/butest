from xml.dom import minidom
from typing import Tuple, List, Dict
import sqlite3


STORE_BASE_URL = 'https://butopea.com'

fetch_products_and_details_sql = 'SELECT p.product_id, pd.name, pd.description, p.image, p.price, m.name FROM product AS p ' \
                                 'LEFT JOIN manufacturer AS m ON p.manufacturer_id == m.manufacturer_id ' \
                                 'LEFT JOIN product_description AS pd ON p.product_id == pd.product_id ' \
                                 'WHERE status != 0'

fetch_ordered_product_images_sql = 'SELECT product_id, image FROM product_image ' \
                                   'ORDER BY CAST(product_id AS INTEGER), CAST(sort_order AS INTEGER)'


def _create_field(root: minidom.Document, parent: minidom.Element, name: str, value: str):
    el = root.createElement(name)
    el.appendChild(root.createTextNode(value))
    parent.appendChild(el)


def _save_xml(doc: minidom.Document):
    xml_str = doc.toprettyxml(indent='\t')
    save_path_file = 'feed.xml'
    with open(save_path_file, 'w') as f:
        f.write(xml_str)


class Product:
    id: str
    title: str
    description: str
    image_link: str
    price: float
    brand: str
    additional_images: List[str]

    def __init__(self,
                 product_id: str,
                 title: str,
                 description: str,
                 image_link: str,
                 price: str,
                 brand: str):
        self.id = product_id
        self.title = title
        self.description = description
        self.image_link = image_link
        self.price = float(price)
        self.brand = brand
        self.additional_images = []

    @staticmethod
    def map_to_product_class(row: Tuple):
        return Product(*row)

    def add_additional_image(self, image_part):
        self.additional_images.append(image_part)

    def build_product_link(self) -> str:
        return f'{STORE_BASE_URL}/p/{self.id}'

    @staticmethod
    def _build_image_url(part: str) -> str:
        return f'{STORE_BASE_URL}/{part}'

    def build_image_link(self) -> str:
        return self._build_image_url(self.image_link)

    def build_iso_price(self) -> str:
        return '{:.2f} HUF'.format(self.price)

    def build_google_spec_item(self, root: minidom.Document) -> minidom.Element:
        item = root.createElement('item')

        _create_field(root, item, 'g:id', self.id)
        _create_field(root, item, 'g:title', self.title)
        _create_field(root, item, 'g:description', self.description)
        _create_field(root, item, 'g:link', self.build_product_link())
        _create_field(root, item, 'g:image_link', self.build_image_link())
        _create_field(root, item, 'g:price', self.build_iso_price())
        _create_field(root, item, 'g:brand', self.brand)
        _create_field(root, item, 'g:availability', 'in_stock')
        _create_field(root, item, 'g:condition', 'new')

        for image in self.additional_images:
            _create_field(root, item, 'g:additional_image_link', self._build_image_url(image))

        return item


def _generate_google_spec_feed(products: List[Product]):
    root = minidom.Document()
    rss = root.createElement('rss')
    rss.setAttribute('version', '2.0')
    rss.setAttribute('xmlns:g', 'http://base.google.com/ns/1.0')
    root.appendChild(rss)

    channel = root.createElement('channel')
    _create_field(root, channel, 'title', 'Butest - Google Product file')
    _create_field(root, channel, 'link', STORE_BASE_URL)
    _create_field(root, channel, 'description', 'RSS feed for products')
    rss.appendChild(channel)

    for product in products:
        item = product.build_google_spec_item(root)
        channel.appendChild(item)

    _save_xml(root)


def main():
    connection = sqlite3.connect('data.sqlite')
    cursor = connection.cursor()

    # fetch product images
    product_id_to_images: Dict[str, List[str]] = {}
    for row in cursor.execute(fetch_ordered_product_images_sql):
        product_id = row[0]
        image_url_part = row[1]

        if product_id not in product_id_to_images:
            product_id_to_images[product_id] = []

        product_id_to_images[product_id].append(image_url_part)

    # fetch products with details
    products: List[Product] = []
    for row in cursor.execute(fetch_products_and_details_sql):
        product = Product.map_to_product_class(row)

        for image in product_id_to_images.get(product.id, []):
            product.add_additional_image(image)

        products.append(product)

    cursor.close()
    connection.close()

    _generate_google_spec_feed(products)


if __name__ == '__main__':
    main()
