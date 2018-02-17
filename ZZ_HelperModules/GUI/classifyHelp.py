
def set_featurematrix_length(final_list):
    featurematrix = []
    # if len(final_list) == 1:
        # featurematrix = [[a] for a in zip(*final_list)]
    if len(final_list) == 3:
        featurematrix = [[a, b, c] for a, b, c in zip(*final_list)]
    elif len(final_list) == 4:
        featurematrix = [[a, b, c, d] for a, b, c, d in zip(*final_list)]
    elif len(final_list) == 9:
        featurematrix = [[a, b, c, d, e, f, g, h, i] for a, b, c, d, e, f, g, h, i in zip(*final_list)]
    elif len(final_list) == 10:
        featurematrix = [[a, b, c, d, e, f, g, h, i, j] for a, b, c, d, e, f, g, h, i, j in zip(*final_list)]
    elif len(final_list) == 12:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l] for
            a, b, c, d, e, f, g, h, i, j, k, l
            in zip(*final_list)]
    elif len(final_list) == 13:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m] for
            a, b, c, d, e, f, g, h, i, j, k, l, m
            in zip(*final_list)]
    elif len(final_list) == 14:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n
            in zip(*final_list)]
    elif len(final_list) == 16:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p
            in zip(*final_list)]
    elif len(final_list) == 17:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q
            in zip(*final_list)]
    elif len(final_list) == 21:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u
            in zip(*final_list)]
    elif len(final_list) == 23:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w
            in zip(*final_list)]
    elif len(final_list) == 25:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y
            in zip(*final_list)]
    elif len(final_list) == 26:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
            in zip(*final_list)]
    elif len(final_list) == 28:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb
            in zip(*final_list)]
    elif len(final_list) == 29:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc
            in zip(*final_list)]
    elif len(final_list) == 34:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh
            in zip(*final_list)]
    elif len(final_list) == 35:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii
            in zip(*final_list)]
    elif len(final_list) == 37:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk
            in zip(*final_list)]
    elif len(final_list) == 38:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll
            in zip(*final_list)]
    elif len(final_list) == 39:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm
            in zip(*final_list)]
    elif len(final_list) == 41:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo
            in zip(*final_list)]
    elif len(final_list) == 42:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp
            in zip(*final_list)]
    elif len(final_list) == 47:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu
            in zip(*final_list)]
    elif len(final_list) == 48:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv
            in zip(*final_list)]
    elif len(final_list) == 50:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx
            in zip(*final_list)]
    elif len(final_list) == 51:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy
            in zip(*final_list)]

    return featurematrix
