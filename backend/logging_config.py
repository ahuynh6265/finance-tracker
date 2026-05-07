import structlog
import logging
import os 

def configure_logging():
  #read env variables, getattr fallback for if attribute does not exist
  app_env = os.environ.get("APP_ENV", "development")
  log_level_name = os.environ.get("LOG_LEVEL", "INFO")
  log_level = getattr(logging, log_level_name.upper(), logging.INFO)

  #different renderers for prod and dev
  if app_env == "production":
    renderer = structlog.processors.JSONRenderer()
  else:
    renderer = structlog.dev.ConsoleRenderer(colors=True)
  
  #used by internal struct logs and foreign stdlib logs for uniform output
  shared_processors = [
    structlog.contextvars.merge_contextvars, #pulls request id from contextvars
    structlog.processors.add_log_level, #add "level: info" to dict 
    structlog.processors.TimeStamper(fmt="iso"), 
    structlog.processors.StackInfoRenderer(), #for when you need to see the log code path with stack_info=True
    structlog.processors.format_exc_info, 
  ]

  #convert internal logs from structlog into stdlib logs 
  structlog.configure(
    processors=shared_processors + [
      structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.make_filtering_bound_logger(log_level), #filter out debug logs
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True 
  )

  #configure stdlib logs  
  formatter = structlog.stdlib.ProcessorFormatter(
    foreign_pre_chain=shared_processors, #format stdlib logs into structlog format 

    #remove _record and _from_structlog fields added with wrap_for_formatter
    processors=[
      structlog.stdlib.ProcessorFormatter.remove_processors_meta, 
      renderer, #final render: json for prod, console for dev
    ],
  )

  handler = logging.StreamHandler()
  handler.setFormatter(formatter)

  root_logger = logging.getLogger()
  root_logger.handlers.clear() #remove any default handlers that uvicorn added 
  root_logger.addHandler(handler)
  root_logger.setLevel(log_level) #filter stdlib-origin debug logs 



