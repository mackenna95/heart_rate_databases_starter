def test_max_adjacent():
    from main import get_info, add_heart_rate, create_user, print_user
    from main import check_tachycardia
    import datetime

    create_user('mackenna96@gmail.com', '23',
                '55', datetime.datetime.now())
    add_heart_rate('mackenna96@gmail.com', '60',
                   datetime.datetime.now())

    user_info = get_info('mackenna96@gmail.com')
    assert user_info.email == 'mackenna96@gmail.com'
    assert user_info.age == 23
    assert user_info.heart_rate == [55, 60]

    user_info = print_user('mackenna96@gmail.com')
    assert user_info.email == 'mackenna96@gmail.com'
    assert user_info.age == 23
    assert user_info.heart_rate == [55, 60]

    tachycardia = check_tachycardia(101, 23)
    assert tachycardia == True
    return
