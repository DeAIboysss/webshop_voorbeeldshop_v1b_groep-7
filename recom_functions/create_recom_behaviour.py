def wipecollaborationfilter(con,cur):
    '''
    Creates empty table to insert filter data into.
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    '''
    cur.execute('DROP TABLE IF EXISTS collaborative_recommendations_behaviour; CREATE TABLE collaborative_recommendations_behaviour(product_id varchar(255),segment varchar(255))')
    con.commit()


def collaborativefilter(nieuwesegments:bool,con,cur):
    '''
    This function collects the data. It then fills the filter with the four most popular products per segment.
    :param nieuwesegments: is een variabele die true is als er segments zijn
    :param con: connection with pgadmin used to commit
    :param cur: cursor in pgadmin used to execute sql
    '''
    if nieuwesegments:
        cur.execute('SELECT DISTINCT segment FROM profile')
        segs = cur.fetchall()
        segments =[]
        for segment in segs:
            if list(segment)[0] is not None and list(segment)[0].lower() not in segments:
                segments.append(list(segment)[0].lower())

    segments = ['leaver', 'bouncer', 'fun_shopper', 'judger', 'browser', 'comparator', 'shopping_cart', 'buyer', 'comparer']

    wipecollaborationfilter(con,cur)

    segmentdict = {}

    cur.execute('''SELECT previously_recommended.productid as product_id,profile.segment FROM profile 
                INNER JOIN previously_recommended ON profileprofile_id = profile.profile_id
                INNER JOIN similars ON similars.profileprofile_id = profile.profile_id
                INNER JOIN viewed_before ON viewed_before.profileprofile_id = profile.profile_id 
                WHERE profile.segment is not null ''')
    products = cur.fetchall()


    for product,seg in products:
        segment = seg.lower()
        if segment in segmentdict.keys():
            if product in segmentdict[segment]:
                segmentdict[segment][product] +=1
            else:
                segmentdict[segment][product] = 1
        else:
            segmentdict[segment] = {product:1}



    for segment in segments:
        highestfreq0 = ['',0]
        highestfreq1 = ['',0]
        highestfreq2 = ['',0]
        highestfreq3 = ['',0]

        id_frequency_dict = segmentdict[segment]
        for id,frequency in id_frequency_dict.items():
            if frequency > highestfreq0[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = highestfreq0
                highestfreq0 = [id,frequency]
            elif frequency > highestfreq1[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = highestfreq1
                highestfreq1 = [id,frequency]
            elif frequency > highestfreq2[1]:
                highestfreq3 = highestfreq2
                highestfreq2 = [id,frequency]
            elif frequency > highestfreq3[1]:
                highestfreq3 = [id,frequency]
        data =[]
        data.append((highestfreq0[0],segment))
        data.append((highestfreq1[0],segment))
        data.append((highestfreq2[0],segment))
        data.append((highestfreq3[0],segment))

        cur.executemany('INSERT INTO collaborative_recommendations_behaviour VALUES(%s,%s)',data)
        con.commit()



