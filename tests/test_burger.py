import pytest
from praktikum.burger import Burger
from unittest.mock import Mock


class TestBurger:

    def test_add_bun(self, burger):                             # добавляем булку
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun is mock_bun

    def test_changing_bun(self, burger):                        # меняем ранее добавленную булку
        first_bun = Mock()
        second_bun = Mock()
        burger.set_buns(first_bun)
        burger.set_buns(second_bun)
        assert burger.bun is second_bun

    def test_add_one_ingredient(self, burger):                   # добавляем один ингридиент
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        assert mock_ingr in burger.ingredients

    def test_add_two_same_ingredients(self, burger):             # добавляем 2 одинаковых ингридиента
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        burger.add_ingredient(mock_ingr)
        assert len(burger.ingredients) == 2
        assert burger.ingredients[0] is mock_ingr
        assert burger.ingredients[1] is mock_ingr

    def test_add_two_different_ingredients(self, burger):         # добавляем 2 разных ингридиента
        mock_ingr_1 = Mock()
        mock_ingr_2 = Mock()
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        assert len(burger.ingredients) == 2
        assert mock_ingr_1 in burger.ingredients
        assert mock_ingr_2 in burger.ingredients

    def test_remove_ingredient(self, burger):                     # удаляем 1 добавленный ранее ингридиент
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0
        assert mock_ingr not in burger.ingredients

    def test_remove_first_ingredient(self, burger):               # удаляем первый ингридиент из списка
        mock_ingr_1 = Mock()
        mock_ingr_2 = Mock()
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        burger.remove_ingredient(0)
        assert burger.ingredients == [mock_ingr_2]

    def test_remove_last_ingredient(self, burger):               # удаляем последний ингридиент из списка
        mock_ingr_1 = Mock()
        mock_ingr_2 = Mock()
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        burger.remove_ingredient(1)
        assert burger.ingredients == [mock_ingr_1]

    def test_move_ingredient(self, burger):                      # передвигаем ингридиент в списке
        mock_ingr_a = Mock()
        mock_ingr_b = Mock()
        mock_ingr_c = Mock()
        burger.add_ingredient(mock_ingr_a)
        burger.add_ingredient(mock_ingr_b)
        burger.add_ingredient(mock_ingr_c)
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [mock_ingr_b, mock_ingr_c, mock_ingr_a]
        assert len(burger.ingredients) == 3

    def test_get_price_only_buns_without_ingridients(self, burger, bun):  # узнаем цену бургера без ингридиентов
        burger.set_buns(bun)
        assert burger.get_price() == 100

    def test_get_price_burger_one_ingridient(self, burger, bun):           # узнаем цену бургера c 1 ингридиентом
        mock_ingr = Mock()
        mock_ingr.get_price.return_value = 30
        burger.set_buns(bun)
        burger.add_ingredient(mock_ingr)
        assert burger.get_price() == 130

    def test_get_price_burger_two_ingridients(self, burger, bun):          # узнаем цену бургера c 2 ингридиентами
        mock_ingr_1 = Mock()
        mock_ingr_1.get_price.return_value = 30
        mock_ingr_2 = Mock()
        mock_ingr_2.get_price.return_value = 40
        burger.set_buns(bun)
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        assert burger.get_price() == 170

    def test_get_get_receipt_burger_without_ingridients(self, burger, bun):          # получаем чек на бургер без ингридиентов
        burger.set_buns(bun)
        receipt = burger.get_receipt()
        assert receipt == (
        "(==== krator bun ====)\n"
        "(==== krator bun ====)\n"
        "\n"
        "Price: 100"
        )

    def test_get_get_receipt_burger_one_ingridient(self, burger, bun):            # чек на бургер c 1 ингридиентом
        mock_ingr = Mock()
        mock_ingr.get_type.return_value = "sause"
        mock_ingr.get_name.return_value = "space"
        mock_ingr.get_price.return_value = 30
        burger.set_buns(bun)
        burger.add_ingredient(mock_ingr)
        receipt = burger.get_receipt()
        assert "(==== krator bun ====)" in receipt
        assert "= sause space =" in receipt
        assert "Price: 130" in receipt

    def test_get_get_receipt_burger_two_ingridients(self, burger, bun):            # чек на бургер c 2 ингридиентами
        mock_filling = Mock()
        mock_filling.get_type.return_value = "filling"
        mock_filling.get_name.return_value = "meat"
        mock_filling.get_price.return_value = 30
        mock_sauce = Mock()
        mock_sauce.get_type.return_value = "sauce"
        mock_sauce.get_name.return_value = "space"
        mock_sauce.get_price.return_value = 20
        burger.set_buns(bun)
        burger.add_ingredient(mock_filling)
        burger.add_ingredient(mock_sauce)
        receipt = burger.get_receipt()
        assert "= filling meat =" in receipt
        assert "= sauce space =" in receipt
        assert "Price: 150" in receipt
