def dfs(tbl_name, constraints, uniq, res):
    """
    perform depth first search
    :param tbl_name:
    :param constraints:
    :param uniq:
    :param res:
    :return:
    """
    if not tbl_name:
        return

    ref_tables = constraints.get(tbl_name, [])
    if not ref_tables:
        return

    for tbl in ref_tables:
        r_tbl_name = tbl.get('foreign_table_name', '')
        if not r_tbl_name:
            continue

        if r_tbl_name in uniq:
            continue

        if r_tbl_name == tbl_name:
            continue

        dfs(r_tbl_name, constraints, uniq, res)
        if r_tbl_name not in uniq:
            uniq.add(r_tbl_name)
            res.append(r_tbl_name)

    if tbl_name not in uniq:
        uniq.add(tbl_name)
        res.append(tbl_name)

    return
