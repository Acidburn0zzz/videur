--
-- main script
--
local util = require "util"
local spec_reader = require "spec_reader"
local body = require "body_reader"


-- read the options from the Nginx config file
local cached_spec = ngx.shared.cached_spec
local spec_url = ngx.var.spec_url or "http://127.0.0.1:8282/api-specs"
local limits, params

-- 1. abort if we don't have any user agent
local key = ngx.var.http_user_agent
if not key then
    return util.bad_request("no user-agent found")
end

-- 2. match the incoming request w/ the spec file and set up $target
ngx.var.target, limits, params = spec_reader.match(spec_url, cached_spec)
local max_size = util.size2int(limits.max_body_size) or util.size2int(ngx.var.max_body_size)

-- 3. control the bozy size
body.check_size(max_size)
