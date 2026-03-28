from django.shortcuts import render


TRACKING_SAMPLE_DATA = {
    "093245135": {
        "tracking_code": "0324135564",
        "recipient_name": "Nguyễn Văn B",
        "recipient_address": "Công Thành, Phong Thái",
        "status": "Giao hàng thành công",
        "created_date": "01/01/2026",
        "estimated_delivery_date": "02/01/2026",
        "timeline": [
            {"label": "Giao thành công", "time": "02/01/2026 09:00", "is_current": True},
            {"label": "Đang giao hàng", "time": "02/01/2026 08:00", "is_current": False},
            {"label": "Xuất kho", "time": "01/01/2026 20:30", "is_current": False},
            {"label": "Tạo đơn hàng", "time": "01/01/2026 20:00", "is_current": False},
        ],
    },
    "0961662268": {
        "tracking_code": "0324135565",
        "recipient_name": "Trần Thị H",
        "recipient_address": "An Lỗ, Phong Hiền, Huế",
        "status": "Đang giao hàng",
        "created_date": "03/01/2026",
        "estimated_delivery_date": "04/01/2026",
        "timeline": [
            {"label": "Đang giao hàng", "time": "04/01/2026 08:30", "is_current": True},
            {"label": "Đã đến bưu cục phát", "time": "04/01/2026 07:45", "is_current": False},
            {"label": "Xuất kho", "time": "03/01/2026 18:15", "is_current": False},
            {"label": "Tạo đơn hàng", "time": "03/01/2026 16:40", "is_current": False},
        ],
    },
}


def _normalize_phone(raw_phone):
    if not raw_phone:
        return ""
    return "".join(character for character in raw_phone if character.isdigit())


def landing_page_view(request):
    searched_phone = request.GET.get("phone", "").strip()
    normalized_phone = _normalize_phone(searched_phone)
    tracking_result = TRACKING_SAMPLE_DATA.get(normalized_phone)

    context = {
        "logo_url": "https://alex.com.vn/Styles/images/logo.svg",
        "poster_url": "https://alex.com.vn/FileUpload/Images/bannerweb_1.jpg",
        "searched_phone": searched_phone,
        "tracking_result": tracking_result,
        "lookup_performed": bool(searched_phone),
        "lookup_not_found": bool(searched_phone) and tracking_result is None,
    }
    return render(request, "home/landing_page.html", context)


def login_page_view(request):
    context = {
        "logo_url": "https://alex.com.vn/Styles/images/logo.svg",
        "poster_url": "https://alex.com.vn/FileUpload/Images/bannerweb_1.jpg",
    }
    return render(request, "home/login_page.html", context)
