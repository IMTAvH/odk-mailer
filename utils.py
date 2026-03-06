processed_ids = set()


def is_duplicate(instance_id):
    if instance_id in processed_ids:
        return True
    processed_ids.add(instance_id)
    return False


EMAIL_CAS_LUA = """
-- KEYS[1] = key del participante (hash)
-- ARGV[1] = nuevo email normalizado
local key = KEYS[1]
local new_email = ARGV[1]

-- 0 = no existe key
if redis.call('EXISTS', key) == 0 then
  return 0
end

-- 1 = email igual, no hacer nada
local current = redis.call('HGET', key, 'email')
if current == new_email then
  return 1
end

-- 2 = email cambiado, Actualiza email
redis.call('HSET', key, 'email', new_email)
return 2
"""
