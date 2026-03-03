"""
Logger utility based on loguru.
Provides singleton pattern for centralized logging.

Usage:
    from src.utils.logger import Logger
    
    logger = Logger()
    logger.info("Test started")
    logger.error("Something went wrong")
"""

from loguru._logger import Logger as LoguruLogger
from loguru import logger as _loguru_logger


class Logger:
    """
    Singleton logger wrapper around loguru.
    
    Usage:
        logger = Logger()
        logger.info("Message")
    """
    _instance: LoguruLogger = None
    
    def __new__(cls) -> "Logger":
        instance = super().__new__(cls)
        if cls._instance is None:
            cls._instance = _loguru_logger
            cls._setup_default()
        return instance
    
    @classmethod
    def _setup_default(cls) -> None:
        """Setup default logger configuration"""
        # Remove default handler
        cls._instance.remove()
        
        # Add console handler with format
        cls._instance.add(
            sink=lambda msg: print(msg, end=""),
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level="INFO",
        )
    
    def __getattr__(self, name: str):
        """Delegate all attribute access to the underlying logger instance"""
        return getattr(self.__class__._instance, name)
    
    # Main logging levels
    def trace(self, message: str, **kwargs) -> None:
        """Log trace level message"""
        self.__class__._instance.trace(message, **kwargs)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug level message"""
        self.__class__._instance.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info level message"""
        self.__class__._instance.info(message, **kwargs)
    
    def success(self, message: str, **kwargs) -> None:
        """Log success level message"""
        self.__class__._instance.success(message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning level message"""
        self.__class__._instance.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error level message"""
        self.__class__._instance.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical level message"""
        self.__class__._instance.critical(message, **kwargs)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback"""
        self.__class__._instance.exception(message, **kwargs)
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton instance (useful for testing)"""
        cls._instance = None


def get_logger() -> LoguruLogger:
    """
    Get logger singleton instance.
    
    Example:
        logger = get_logger()
        logger.info("Test started")
        logger.error("Something went wrong")
    """
    return Logger._get_instance()


def reset_logger() -> None:
    """
    Reset logger singleton.
    Useful for testing when you need to reconfigure logging.
    """
    Logger.reset()
