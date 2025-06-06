"""Streaming-related type definitions for the SDK.

These types are modeled after the Bedrock API.

- Bedrock docs: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Types_Amazon_Bedrock_Runtime.html
"""

from typing import Optional, Union

from typing_extensions import TypedDict

from .content import ContentBlockStart, Role
from .event_loop import Metrics, StopReason, Usage
from .guardrails import Trace


class MessageStartEvent(TypedDict):
    """Event signaling the start of a message in a streaming response.

    Attributes:
        role: The role of the message sender (e.g., "assistant", "user").
    """

    role: Role


class ContentBlockStartEvent(TypedDict, total=False):
    """Event signaling the start of a content block in a streaming response.

    Attributes:
        contentBlockIndex: Index of the content block within the message.
            This is optional to accommodate different model providers.
        start: Information about the content block being started.
    """

    contentBlockIndex: Optional[int]
    start: ContentBlockStart


class ContentBlockDeltaText(TypedDict):
    """Text content delta in a streaming response.

    Attributes:
        text: The text fragment being streamed.
    """

    text: str


class ContentBlockDeltaToolUse(TypedDict):
    """Tool use input delta in a streaming response.

    Attributes:
        input: The tool input fragment being streamed.
    """

    input: str


class ReasoningContentBlockDelta(TypedDict, total=False):
    """Delta for reasoning content block in a streaming response.

    Attributes:
        redactedContent: The content in the reasoning that was encrypted by the model provider for safety reasons.
        signature: A token that verifies that the reasoning text was generated by the model.
        text: The reasoning that the model used to return the output.
    """

    redactedContent: Optional[bytes]
    signature: Optional[str]
    text: Optional[str]


class ContentBlockDelta(TypedDict, total=False):
    """A block of content in a streaming response.

    Attributes:
        reasoningContent: Contains content regarding the reasoning that is carried out by the model.
        text: Text fragment being streamed.
        toolUse: Tool use input fragment being streamed.
    """

    reasoningContent: ReasoningContentBlockDelta
    text: str
    toolUse: ContentBlockDeltaToolUse


class ContentBlockDeltaEvent(TypedDict, total=False):
    """Event containing a delta update for a content block in a streaming response.

    Attributes:
        contentBlockIndex: Index of the content block within the message.
            This is optional to accommodate different model providers.
        delta: The incremental content update for the content block.
    """

    contentBlockIndex: Optional[int]
    delta: ContentBlockDelta


class ContentBlockStopEvent(TypedDict, total=False):
    """Event signaling the end of a content block in a streaming response.

    Attributes:
        contentBlockIndex: Index of the content block within the message.
            This is optional to accommodate different model providers.
    """

    contentBlockIndex: Optional[int]


class MessageStopEvent(TypedDict, total=False):
    """Event signaling the end of a message in a streaming response.

    Attributes:
        additionalModelResponseFields: Additional fields to include in model response.
        stopReason: The reason why the model stopped generating content.
    """

    additionalModelResponseFields: Optional[Union[dict, list, int, float, str, bool, None]]
    stopReason: StopReason


class MetadataEvent(TypedDict, total=False):
    """Event containing metadata about the streaming response.

    Attributes:
        metrics: Performance metrics related to the model invocation.
        trace: Trace information for debugging and monitoring.
        usage: Resource usage information for the model invocation.
    """

    metrics: Metrics
    trace: Optional[Trace]
    usage: Usage


class ExceptionEvent(TypedDict):
    """Base event for exceptions in a streaming response.

    Attributes:
        message: The error message describing what went wrong.
    """

    message: str


class ModelStreamErrorEvent(ExceptionEvent):
    """Event for model streaming errors.

    Attributes:
        originalMessage: The original error message from the model provider.
        originalStatusCode: The HTTP status code returned by the model provider.
    """

    originalMessage: str
    originalStatusCode: int


class RedactContentEvent(TypedDict, total=False):
    """Event for redacting content.

    Attributes:
        redactUserContentMessage: The string to overwrite the users input with.
        redactAssistantContentMessage: The string to overwrite the assistants output with.

    """

    redactUserContentMessage: Optional[str]
    redactAssistantContentMessage: Optional[str]


class StreamEvent(TypedDict, total=False):
    """The messages output stream.

    Attributes:
        contentBlockDelta: Delta content for a content block.
        contentBlockStart: Start of a content block.
        contentBlockStop: End of a content block.
        internalServerException: Internal server error information.
        messageStart: Start of a message.
        messageStop: End of a message.
        metadata: Metadata about the streaming response.
        modelStreamErrorException: Model streaming error information.
        serviceUnavailableException: Service unavailable error information.
        throttlingException: Throttling error information.
        validationException: Validation error information.
    """

    contentBlockDelta: ContentBlockDeltaEvent
    contentBlockStart: ContentBlockStartEvent
    contentBlockStop: ContentBlockStopEvent
    internalServerException: ExceptionEvent
    messageStart: MessageStartEvent
    messageStop: MessageStopEvent
    metadata: MetadataEvent
    redactContent: RedactContentEvent
    modelStreamErrorException: ModelStreamErrorEvent
    serviceUnavailableException: ExceptionEvent
    throttlingException: ExceptionEvent
    validationException: ExceptionEvent
