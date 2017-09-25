
from sqlalchemy import create_engine, asc
import sqlalchemy.orm
from sqlalchemy.orm import exc

from hamal.utils import config
from hamal.db import models as db_models


_ENGINE = None
_SESSION_MAKER = None

def get_engine():
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    myconfig = config.config_module('/etc/hamal/hamal.conf')
    _ENGINE = create_engine(myconfig.get_string("mysql", "db_connect", "mysql://root:xxx@127.0.0.1/mytest?charset=utf8"))
    return _ENGINE

def _get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER

    _SESSION_MAKER = sqlalchemy.orm.sessionmaker(bind=engine)
    return _SESSION_MAKER

def _tuple_to_model(model_instance, result_set, *args):
    for key, value in enumerate(args):
        setattr(model_instance, value, result_set[key])
    return model_instance

def _get_session():
    engine = get_engine()
    maker = _get_session_maker(engine)
    session = maker()

    return session

##### Region OPT ####
##### select
def region_get_all(*args):
    if not args or len(args) == 0:
        query = _get_session().query(db_models.Region)
    else:
        query = _get_session().query(*args).select_from(db_models.Region)
    results = query.all()
    return results  if not args or len(args) == 0 else \
           [_tuple_to_model(db_models.Region(), result, *args) for result in results if results and len(results) > 0]

def region_get_by_uuid(uuid, *args):
    if not args or len(args) == 0:
        query = _get_session().query(db_models.Region).filter_by(uuid=uuid)
    else:
        query = _get_session().query(*args).select_from(db_models.Region) \
                .filter_by(uuid=uuid)
    try:
        region = query.one()
    except exc.NoResultFound:
        # TODO(developer): process this situation
        pass

    return region if not args or len(args) == 0 else \
        _tuple_to_model(db_models.Region(), region, *args)

#####  add
def region_set_one(region):
    session = _get_session()
    session.add(region)
    session.commit()

def region_set_mul(region_list):
    session = _get_session()
    session.add_all(region_list)
    session.commit()
#####  update
def region_set_by_uuid(uuid, kvmap):
    session = _get_session()
    session.query(db_models.Region).filter_by(uuid=uuid).update(kvmap)
    session.commit()
#####  delete
def region_del_by_uuid(uuid):
    session = _get_session()
    region = session.query(db_models.Region).filter_by(uuid=uuid).one()
    session.delete(region)
    session.commit()

def region_get_by_condition_with_order(orderby, *args, **condition):
    query = _get_session().query(db_models.Region) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Region)
    query = query if not condition else query.filter_by(**condition)
    query = query if not orderby else query.order_by(orderby)
    results = query.all()
    return results if not args or len(args) == 0 else \
           [_tuple_to_model(db_models.Region(), result, *args) for result in results if results and len(results) > 0]
        

##### Region OPT ####

##### Rack OPT ####
def rack_get_all(*args):
    query = _get_session().query(db_models.Rack) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Rack)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Rack(), result, *args) for result in results if results and len(results) > 0]

def rack_get_by_uuid(uuid, *args):
    if not args or len(args) == 0:
        query = _get_session().query(db_models.Rack).filter_by(uuid=uuid)
    else:
        query = _get_session().query(*args).select_from(db_models.Rack) \
                .filter_by(uuid=uuid)
    try:
        rack = query.one()
    except exc.NoResultFound:
        # TODO(developer): process this situation
        pass
    return rack if not args or len(args) == 0 else _tuple_to_model(db_models.Rack(), rack, *args)
#####  add
def rack_set_one(rack):
    session = _get_session()
    session.add(rack)
    session.commit()

def rack_set_mul(rack_list):
    session = _get_session()
    session.add_all(rack_list)
    session.commit()
#####  update
def rack_set_by_uuid(uuid, kvmap):
    session = _get_session()
    session.query(db_models.Rack).filter_by(uuid=uuid).update(kvmap)
    session.commit()
#####  delete
def rack_del_by_uuid(uuid):
    session = _get_session()
    rack = session.query(db_models.Rack).filter_by(uuid=uuid).one()
    session.delete(rack)
    session.commit()
    
def rack_get_by_condition_with_order(orderby, *args, **condition):
    query = _get_session().query(db_models.Rack) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Rack)
    query = query if not condition else query.filter_by(**condition)
    query = query if not orderby else query.order_by(orderby)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Rack(), result, *args) for result in results if results and len(results) > 0]

    
##### Rack OPT ####

##### Node OPT ####
def node_get_all(*args):
    query = _get_session().query(db_models.Node) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Node)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Node(), result, *args) for result in results if results and len(results) > 0]

def node_get_by_uuid(uuid, *args):
    if not args or len(args) == 0:
        query = _get_session().query(db_models.Node).filter_by(uuid=uuid)
    else:
        query = _get_session().query(*args).select_from(db_models.Node) \
                .filter_by(uuid=uuid)
    try:
        node = query.one()
    except exc.NoResultFound:
        # TODO(developer): process this situation
        pass
    return node if not args or len(args) == 0 else _tuple_to_model(db_models.Node(), node, *args)
#####  add
def node_set_one(node):
    session = _get_session()
    session.add(node)
    session.commit()

def node_set_mul(node_list):
    session = _get_session()
    session.add_all(node_list)
    session.commit()
#####  update
def node_set_by_uuid(uuid, kvmap):
    session = _get_session()
    session.query(db_models.Node).filter_by(uuid=uuid).update(kvmap)
    session.commit()
#####  delete
def node_del_by_uuid(uuid):
    session = _get_session()
    node = session.query(db_models.Node).filter_by(uuid=uuid).one()
    session.delete(node)
    session.commit()

def node_get_by_condition_with_order(orderby, *args, **condition):
    query = _get_session().query(db_models.Node) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Node)
    query = query if not condition else query.filter_by(**condition)
    query = query if not orderby else query.order_by(orderby)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Node(), result, *args) for result in results if results and len(results) > 0]
##### Node OPT ####

##### Role OPT ####
def role_get_all(*args):
    query = _get_session().query(db_models.Role) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Role)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Role(), result, *args) for result in results if results and len(results) > 0]

def role_get_by_condition_with_order(order_by, *args, **condition):
    query = _get_session().query(db_models.Role) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Role)
    query = query if not condition else query.filter_by(**condition)
    query = query if not order_by else query.order_by(asc(order_by))
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Role(), result, *args) for result in results if results and len(results) > 0]

def role_get_by_uuid(uuid, *args):
    if not args or len(args) == 0:
        query = _get_session().query(db_models.Role).filter_by(uuid=uuid)
    else:
        query = _get_session().query(*args).select_from(db_models.Role) \
                .filter_by(uuid=uuid)
    try:
        role = query.one()
    except exc.NoResultFound:
        # TODO(developer): process this situation
        pass
    return role if not args or len(args) == 0 else _tuple_to_model(db_models.Role(), role, *args)
#####  add
def role_set_one(role):
    session = _get_session()
    session.add(role)
    session.commit()

def role_set_mul(role_list):
    session = _get_session()
    session.add_all(role_list)
    session.commit()
#####  update
def role_set_by_uuid(uuid, kvmap):
    session = _get_session()
    session.query(db_models.Role).filter_by(uuid=uuid).update(kvmap)
    session.commit()
#####  delete
def role_del_by_uuid(uuid):
    session = _get_session()
    role = session.query(db_models.Role).filter_by(uuid=uuid).one()
    session.delete(role)
    session.commit()
##### Role OPT ####

##### Relation OPT ####
def relation_get_all(*args):
    query = _get_session().query(db_models.Relation) if not args or len(args) == 0 \
           else _get_session().query(*args).select_from(db_models.Relation)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Relation(), result, *args) for result in results if results and len(results) > 0]

def relation_get_by_condition_with_order(orderby, *args, **condition):
    query = _get_session().query(db_models.Relation) if not args or len(args) == 0 \
            else _get_session().query(*args).select_from(db_models.Relation)
    query = query if not condition else query.filter_by(**condition)
    query = query if not orderby else query.order_by(orderby)
    results = query.all()
    return results if not args or len(args) == 0 else \
        [_tuple_to_model(db_models.Relation(), result, *args) for result in results if results and len(results) > 0]
#####  add
def relation_set_one(relation):
    session = _get_session()
    session.add(relation)
    session.commit()

def relation_set_mul(relation_list):
    session = _get_session()
    session.add_all(relation_list)
    session.commit()
#####  update
def relation_set_by_uuid(uuid, kvmap):
    session = _get_session()
    session.query(db_models.Relation).filter_by(uuid=uuid).update(kvmap)
    session.commit()
#####  delete
def relation_del_by_uuid(uuid):
    session = _get_session()
    relation = session.query(db_models.Relation).filter_by(uuid=uuid).one()
    session.delete(relation)
    session.commit()
##### Relation OPT ####
