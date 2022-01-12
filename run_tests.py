from test_cases import test_get_categories, test_get_blog_categories, test_post_categories, test_put_categories, \
    test_delete_cateogries
import unittest


def run_tests():
    for test_module in [test_get_categories, test_get_blog_categories, test_post_categories,
                        test_put_categories, test_delete_cateogries]:
        suite = unittest.TestLoader().loadTestsFromModule(test_module)
        unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    run_tests()
