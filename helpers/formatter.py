def rupiah(angka):

    return "Rp {:,.0f}".format(
        float(angka)
    ).replace(",", ".")