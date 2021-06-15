# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from products.models import Category, Subcategory, Product, db_connect, create_table


class SaveProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """Save product in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        product = Product()
        subcategory = Subcategory()
        category = Category()
        product.name = item["title"]
        product.source = item["source"]
        if 'rate' in item:
            product.rate = item["rate"]
        if 'safety' in item:
            product.safety = item["safety"]
        if 'quality' in item:
            product.quality = item["quality"]
        subcategory.name = item["subcategory"]
        category.name = item["category"]

        # Check for product duplicate
        exist_product = session.query(Product).filter_by(name = product.name).first()
        if exist_product is not None:
            exist_product.rate = product.rate
            exist_product.safety = product.safety
            exist_product.quality = product.quality
            exist_product.source = product.source
        else:
             # Check for subcategory duplicate
            exist_subcategory = session.query(Subcategory).filter_by(name = subcategory.name).first()
            if exist_subcategory is not None:
                exist_subcategory.products.append(product)
            else:
                subcategory.products.append(product)
                 # Check for category duplicate
                exist_category = session.query(Category).filter_by(name = category.name).first()
                if exist_category is not None:
                    exist_category.subcategories.append(subcategory)
                else:
                    category.subcategories.append(subcategory)
            
            try:
                session.add(product)
            except:
                session.rollback()
                raise

        try:
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
