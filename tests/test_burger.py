import pytest
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

    def test_add_one_ingredient(self, burger):                   # добавляем один ингредиент
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        assert mock_ingr in burger.ingredients

    def test_add_two_same_ingredients(self, burger):             # добавляем 2 одинаковых ингредиента
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        burger.add_ingredient(mock_ingr)
        assert burger.ingredients == [mock_ingr, mock_ingr]

    def test_add_two_different_ingredients(self, burger):         # добавляем 2 разных ингредиента
        mock_ingr_1 = Mock()
        mock_ingr_2 = Mock()
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        assert burger.ingredients == [mock_ingr_1, mock_ingr_2]

    def test_remove_only_ingredient(self, burger):               # удаляем 1 единственный ингредиент
        mock_ingr = Mock()
        burger.add_ingredient(mock_ingr)
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    @pytest.mark.parametrize(                                    # удаляем ингредиенты из списка
        "inx, final_inx",
        [(0, [1]), (1, [0])],                                    
        ids=["remove_first_ingr", "remove_last_ingr"]
        )
    def test_remove_ingredient(self, burger, inx, final_inx):  
        mock_ingr_1 = Mock()
        mock_ingr_2 = Mock()
        ingredients = [mock_ingr_1, mock_ingr_2]
        burger.add_ingredient(mock_ingr_1)
        burger.add_ingredient(mock_ingr_2)
        burger.remove_ingredient(inx)
        assert burger.ingredients == [ingredients[i] for i in final_inx]

    @pytest.mark.parametrize(                                    # передвигаем ингредиенты в списке
        "inx, new_inx, final_order",
        [(0, 2, [1, 2, 0]), (2, 0, [2, 0, 1])],                  # вперед, назад
        ids=["move_forward", "move_backward"]
        )
    def test_move_ingredient(self, burger, inx, new_inx, final_order):                      
        mock_ingr_a = Mock()
        mock_ingr_b = Mock()
        mock_ingr_c = Mock()
        ingredients = [mock_ingr_a, mock_ingr_b, mock_ingr_c]
        burger.add_ingredient(mock_ingr_a)
        burger.add_ingredient(mock_ingr_b)
        burger.add_ingredient(mock_ingr_c)
        burger.move_ingredient(inx, new_inx)
        assert burger.ingredients == [ingredients[i] for i in final_order]

    @pytest.mark.parametrize(                                     # узнаем цену бургера
        "ingr_prices, final_price",
        [([], 100), ([30], 130), ([30, 40], 170)],                # без ингр-тов, с 1 ингр-том, с 2 ингр-тами
        ids=["without_ingr", "one_ingr", "two_ingr"]
        )
    def test_get_price(self, burger, bun, ingr_prices, final_price):
        burger.set_buns(bun)
        for price in ingr_prices:
            mock_ingr = Mock()
            mock_ingr.get_price.return_value = price
            burger.add_ingredient(mock_ingr)
        assert burger.get_price() == final_price
        
    def test_get_receipt_without_ingredients(self, burger, bun):    # получаем чек на бургер без ингр-тов
        burger.set_buns(bun)
        receipt = burger.get_receipt()
        assert receipt == (
        "(==== krator bun ====)\n"
        "(==== krator bun ====)\n"
        "\n"
        "Price: 100"
        )

    @pytest.mark.parametrize(                                              # получаем чек на бургер c ингр-тами
        "ingr_spec, final_lines, final_price",
        [
        ([("space", "sauce", 30)], ["= sauce space ="], 130),
        ([("meat", "filling", 30), ("space", "sauce", 20)], ["= filling meat =", "= sauce space ="], 150),
        ],
        ids=["one_ingr", "two_ingr"],
        )
    def test_get_receipt_burger_with_ingredients(self, burger, bun, ingr_spec, final_lines, final_price):           
        burger.set_buns(bun)
        for ingr_name, ingr_type, price in ingr_spec:
            mock_ingr = Mock()
            mock_ingr.get_name.return_value = ingr_name
            mock_ingr.get_type.return_value = ingr_type
            mock_ingr.get_price.return_value = price
            burger.add_ingredient(mock_ingr)
        receipt = burger.get_receipt()
        assert "(==== krator bun ====)" in receipt
        for line in final_lines:
            assert line in receipt
        assert f"Price: {final_price}" in receipt
