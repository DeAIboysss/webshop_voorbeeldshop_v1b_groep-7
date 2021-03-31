def collect_contentfilter(profileid,cur):
    cur = cur
    product_ids2 = []
    cur.execute("SELECT segment FROM profile WHERE profile_id = '%s'"%(profileid))
    segment = cur.fetchall()
    segment = list(segment)[0][0]
    print(segment)
    if type(segment) == type(None) or segment == 'bouncer' or segment == 'leaver':
        segment = 'buyer'
    else:
        segment = segment.lower()
    print(segment)
    cur.execute("SELECT product_id FROM collaborative_recommendations_behaviour WHERE segment = '%s'"%(segment))
    product_ids = cur.fetchall()
    for i in list(product_ids):
        product_ids2.append(i[0])

    return product_ids2

